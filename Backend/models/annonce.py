from sqlalchemy import Column, String, Boolean, DateTime, Float, DECIMAL, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Annonce(Base):
    __tablename__ = "annonces"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titre = Column(String(255), nullable=False)
    description = Column(String(1000))
    prix = Column(DECIMAL(10, 2))
    categorie = Column(String(100))
    lieu = Column(String(255))
    dateCreation = Column(DateTime, default=datetime.utcnow)
    utilisateurId = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    active = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
