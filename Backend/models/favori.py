from sqlalchemy import Column, String, ForeignKey
import uuid
from config.db import Base

class Favori(Base):
    __tablename__ = "favoris"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    utilisateurId = Column(String, ForeignKey("utilisateurs.id"), nullable=False)
    annonceId = Column(String, ForeignKey("annonces.id"), nullable=False)
