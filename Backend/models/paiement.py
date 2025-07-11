from sqlalchemy import Column, String, DateTime, DECIMAL, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    utilisateurId = Column(String, ForeignKey("utilisateurs.id"), nullable=False)
    annonceId = Column(String, ForeignKey("annonces.id"), nullable=False)
    montant = Column(DECIMAL, nullable=False)
    statut = Column(String, nullable=False)
    dateCreation = Column(DateTime, default=datetime.utcnow)
