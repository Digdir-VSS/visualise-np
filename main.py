from fastapi import FastAPI, HTTPException
from typing import Any
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os 
from database.db_connection import DBConnector
from pydantic import BaseModel

load_dotenv()

db_client = DBConnector.create_engine(
        os.getenv("DRIVER"),
        os.getenv("SERVER"),
        os.getenv("DATABASE"),
        os.getenv("FABRIC_CLIENT_ID"),
        os.getenv("TENANT_ID"),
        os.getenv("FABRIC_SECRET"))

class Dataset(BaseModel):
    label: str
    data: list[Any]

class ChartResponse(BaseModel):
    type: str
    labels: list[str]
    datasets: list[Dataset]

app = FastAPI()

@app.get("/api/tiltak-per-kommune", response_model=ChartResponse)
def get_tiltak_per_kommune():
    try:
        tiltak = db_client.get_all_tiltak()
        virksomheter = db_client.get_all_virksomheter()
    except Exception as e:
        raise HTTPException(status_code=503, detail="Kunne ikke hente data fra databasen")

    try:
        kommune_lookup = {
            v.organisasjonsnummer: v.kommune or "Ukjent"
            for v in virksomheter
        }

        counts = {}
        for t in tiltak:
            kommune = kommune_lookup.get(t.virksomhet_organisasjonsnummer, "Ukjent")
            counts[kommune] = counts.get(kommune, 0) + 1

        return ChartResponse(
            type="bar",
            labels=list(counts.keys()),
            datasets=[Dataset(label="Antall tiltak", data=list(counts.values()))]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Feil ved behandling av data")

@app.get("/charts/tiltak-per-kommune", response_class=HTMLResponse)
def chart_virksomheter():
    with open("static/kommune_per_tiltak_chart.html") as f:
        return HTMLResponse(content=f.read())