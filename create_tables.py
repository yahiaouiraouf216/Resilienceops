from app.database import Base, engine
from app.models import Ticket, Incident, IncidentEvent, ChaosExperiment

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
