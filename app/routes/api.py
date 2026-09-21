from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    Ticket,
    Incident,
    IncidentEvent,
    ChaosExperiment
)

router = APIRouter(prefix="/api")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# DASHBOARD STATS
# =========================

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    tickets = db.query(Ticket).count()

    active_incidents = (
        db.query(Incident)
        .filter(Incident.status != "Resolved")
        .count()
    )

    resolved_incidents = (
        db.query(Incident)
        .filter(Incident.status == "Resolved")
        .count()
    )

    chaos_experiments = db.query(ChaosExperiment).count()

    return {
        "tickets": tickets,
        "active_incidents": active_incidents,
        "resolved_incidents": resolved_incidents,
        "chaos_experiments": chaos_experiments
    }


# =========================
# TICKETS
# =========================

@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.id.desc()).all()


@router.post("/tickets")
def create_ticket(
    title: str,
    description: str = "",
    priority: str = "Medium",
    db: Session = Depends(get_db)
):

    ticket = Ticket(
        title=title,
        description=description,
        priority=priority
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


# =========================
# INCIDENTS
# =========================

@router.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.id.desc()).all()


@router.post("/incidents")
def create_incident(
    title: str,
    description: str = "",
    severity: str = "Medium",
    db: Session = Depends(get_db)
):

    incident = Incident(
        title=title,
        description=description,
        severity=severity
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.post("/incidents/{incident_id}/events")
def add_incident_event(
    incident_id: int,
    event_type: str,
    message: str,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    event = IncidentEvent(
        incident_id=incident_id,
        event_type=event_type,
        message=message
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.get("/incidents/{incident_id}/timeline")
def get_incident_timeline(
    incident_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(IncidentEvent)
        .filter(IncidentEvent.incident_id == incident_id)
        .order_by(IncidentEvent.created_at)
        .all()
    )


# =========================
# CHAOS
# =========================

@router.get("/chaos")
def get_chaos_experiments(
    db: Session = Depends(get_db)
):
    return (
        db.query(ChaosExperiment)
        .order_by(ChaosExperiment.id.desc())
        .all()
    )


@router.post("/chaos")
def create_chaos_experiment(
    name: str,
    experiment_type: str,
    description: str = "",
    db: Session = Depends(get_db)
):

    experiment = ChaosExperiment(
        name=name,
        experiment_type=experiment_type,
        description=description
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    return experiment