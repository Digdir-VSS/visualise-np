from typing import List
import struct
from azure.identity import ClientSecretCredential
import urllib
from sqlmodel import Session, select
from sqlalchemy import create_engine, event, Engine
from azure.identity import ClientSecretCredential

from database.datamodels import Virksomhet, Tiltak

from dotenv import load_dotenv

load_dotenv()

class DBConnector:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    @classmethod
    def create_engine(
        cls,
        driver_name: str,
        server_name: str,
        database_name: str,
        fabric_client_id: str,
        fabric_tenant_id: str,
        fabric_client_secret: str,
    ):
        # --- Connection string (NO auth here, token comes later) ---
        connection_string = (
            "Driver={};Server=tcp:{},1433;Database={};Encrypt=yes;"
            "TrustServerCertificate=no;Connection Timeout=30; encoding=utf8"
        ).format(driver_name, server_name, database_name)

        params = urllib.parse.quote(connection_string)
        odbc_str = f"mssql+pyodbc:///?odbc_connect={params}"

        engine = create_engine(
            odbc_str, echo=False, pool_pre_ping=True, pool_recycle=3600, pool_timeout=30
        )

        credential = ClientSecretCredential(
            tenant_id=fabric_tenant_id,
            client_id=fabric_client_id,
            client_secret=fabric_client_secret,
        )  # or ClientSecretCredential if you prefer

        @event.listens_for(engine, "do_connect")
        def provide_token(dialect, conn_rec, cargs, cparams):
            token_bytes = credential.get_token(
                "https://database.windows.net/.default"
            ).token.encode("utf-16-le")
            token_struct = struct.pack(
                f"<I{len(token_bytes)}s", len(token_bytes), token_bytes
            )
            SQL_COPT_SS_ACCESS_TOKEN = 1256
            cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}
        
        return cls(engine)
    
    def get_all_virksomheter(self) -> List[Virksomhet]:
        with Session(self.engine) as session:
            result = session.exec(select(Virksomhet)).all()
            return result

    def get_all_tiltak(self) -> List[Tiltak]:
        with Session(self.engine) as session:
            result = session.exec(select(Tiltak)).all()
            return result
