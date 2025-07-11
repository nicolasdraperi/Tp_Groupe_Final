from sqlalchemy import Column, String, Boolean, DateTime, Float, DECIMAL, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Annonce(Base):
    __tablename__ = "annonces"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titre = Column(String, nullable=False)
    description = Column(String)
    prix = Column(DECIMAL)
    categorie = Column(String)
    lieu = Column(String)
    dateCreation = Column(DateTime, default=datetime.utcnow)
    utilisateurId = Column(String, ForeignKey("utilisateurs.id"), nullable=False)
    active = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
