from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Alerte(Base):
    __tablename__ = "alertes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    utilisateurId = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    message = Column(String(1000), nullable=False)
    dateEnvoi = Column(DateTime, default=datetime.utcnow)
    lu = Column(Boolean, default=False)
