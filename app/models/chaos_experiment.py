from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base


class ChaosExperiment(Base):
    __tablename__ = "chaos_experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    experiment_type = Column(String(50), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

