from sqlalchemy import Column, String, DateTime, DECIMAL, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    utilisateurId = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    annonceId = Column(String(36), ForeignKey("annonces.id"), nullable=False)
    montant = Column(DECIMAL(10, 2), nullable=False)
    statut = Column(String(50), nullable=False)
    dateCreation = Column(DateTime, default=datetime.utcnow)
