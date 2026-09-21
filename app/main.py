from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routes.api import router

app = FastAPI(title="ResilienceOps")

DASHBOARD = Path(__file__).parent / "templates" / "dashboard.html"


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD.read_text()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "resilienceops"
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
        "service": "resilienceops"
    }


app.include_router(router)