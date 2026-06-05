# Visualisering av data med FastAPI og Chart.js

Dette prosjektet eksponerer diagram via FastAPI-endepunkter som kan bygges inn i Drupal via `<iframe>`.

---

## Hvordan det fungerer

Systemet består av tre deler som jobber sammen:

**FastAPI (Python)** — serverer to typer endepunkter:
- `/api/...` — returnerer data som JSON
- `/charts/...` — returnerer en HTML-side med diagrammet

**HTML-filen** — en enkel side med en `<canvas>`-element og Chart.js innebygd. Henter data fra `/api/`-endepunktet og tegner diagrammet i nettleseren.

---

## Prosjektstruktur

```
├── main.py                          ← FastAPI-endepunkter og datalogikk
├── database/
│   ├── db_connection.py             ← Databaseklient, kun rådata
│   └── datamodels.py                ← SQLModel-modeller
├── static/
│   └── tiltak_per_kommune.html      ← HTML med Chart.js per diagram
└── .env                             ← Miljøvariabler
```

---

## Slik legger du til et nytt diagram

### 1. Legg til datalogikk i `main.py`

```python
@app.get("/api/mitt-nye-diagram", response_model=ChartResponse)
def get_mitt_nye_diagram():
    # Hent rådata fra databasen
    data = db_client.get_all_tiltak()

    # Aggreger / beregn det du vil vise
    counts = {}
    for t in data:
        key = t.status or "Ukjent"
        counts[key] = counts.get(key, 0) + 1

    return ChartResponse(
        type="bar",
        labels=list(counts.keys()),
        datasets=[Dataset(label="Antall", data=list(counts.values()))]
    )
```

### 2. Lag HTML-filen i `static/`

Opprett `static/mitt_nye_diagram.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <canvas id="chart"></canvas>
  <script>
    async function render() {
      const response = await fetch('/api/mitt-nye-diagram');
      const data = await response.json();

      new Chart(document.getElementById('chart'), {
        type: data.type,
        data: {
          labels: data.labels,
          datasets: data.datasets,
        },
        options: {
          responsive: true,
        }
      });
    }
    render();
  </script>
</body>
</html>
```

### 3. Legg til HTML-endepunktet i `main.py`

```python
@app.get("/charts/mitt-nye-diagram", response_class=HTMLResponse)
def chart_mitt_nye_diagram():
    with open("static/mitt_nye_diagram.html") as f:
        return HTMLResponse(content=f.read())
```

---

## Miljøvariabler

Opprett en `.env`-fil i rotkatalogen:

```
DRIVER=ODBC Driver 18 for SQL Server
SERVER=din-server.database.windows.net
DATABASE=ditt-databasenavn
SCHEMA=ditt-schema
FABRIC_CLIENT_ID=din-client-id
TENANT_ID=din-tenant-id
FABRIC_SECRET=din-hemmelighet
```

---

## Kjøre lokalt

```bash
uv sync
uvicorn main:app --reload
```

Åpne `http://localhost:8000/charts/tiltak-per-kommune` i nettleseren.