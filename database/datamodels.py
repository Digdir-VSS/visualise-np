from typing import Any, Dict, Optional
from datetime import date, datetime
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field

load_dotenv()

load_dotenv()

class Virksomhet(SQLModel, table=True):
    __tablename__ = "Virksomhet"
    __table_args__ = {"schema": os.getenv("SCHEMA")}
    organisasjonsnummer: str = Field(primary_key=True)
    navn:                   Optional[str] = None
    departement_navn:       Optional[str] = None
    departement_orgnr:      Optional[str] = None
    addresse:               Optional[str] = None
    kommune:                Optional[str] = None
    organisasjonsform:      Optional[str] = None  
    land:                   Optional[str] = None   
    poststed:               Optional[str] = None   

class Kontaktperson(SQLModel, table=True):
    __tablename__ = "Kontaktperson"
    __table_args__ = {"schema": os.getenv("SCHEMA")}
    record_id: str = Field(primary_key=True)
    navn:  Optional[str] = None
    stilling: Optional[str] = None
    telefon: Optional[str] = None
    epost: Optional[str] = None
    

class Tiltak(SQLModel, table=True):
    __tablename__ = "Tiltak"
    __table_args__ = {"schema": os.getenv("SCHEMA")}

    record_id: str = Field(primary_key=True)
    navn: str
    kontakt_person: Optional[str]
    beskrivelse: Optional[str] = None
    fag_temaomrade: Optional[str] = None
    formal_hensikt: Optional[str] = None
    problemstilling: Optional[str] = None
    oppstartsdato: Optional[date] = None
    strategisk_omrade: Optional[str] = None
    sluttdato: Optional[date] = None
    finanseringskilde: Optional[str] = None
    status: Optional[str] = None
    intern_tverrgaande: Optional[str] = None
    avhengigheter: Optional[str] = None
    virksomhet_organisasjonsnummer: str

    kortnavn: Optional[str] = None
    departement_navn: Optional[str] = None
    kostnadsramme: Optional[str] = None
    digitalisering_rundskriv: Optional[str] = None
    teknologi: Optional[str] = None

class Portefølje(SQLModel, table=True):
    __tablename__ = "Portefølje"
    __table_args__ = {"schema": os.getenv("SCHEMA")}

    record_id: str = Field(primary_key=True)
    navn: str
    tiltak_id: str

class SamarbeidendeVirksomhet(SQLModel, table=True):
    __tablename__ = "SamarbeidendeVirksomhet"
    __table_args__ = {"schema": os.getenv("SCHEMA")}

    organisasjonsnummer: str = Field(primary_key=True)
    navn:                   Optional[str] = None
    departement_navn:       Optional[str] = None
    departement_orgnr:      Optional[str] = None
    addresse:               Optional[str] = None
    kommune:                Optional[str] = None
    organisasjonsform:      Optional[str] = None  
    land:                   Optional[str] = None   
    poststed:               Optional[str] = None   
    tiltak_record_id: str