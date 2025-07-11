from sqlalchemy import Column, String, Boolean, DateTime
import uuid
from datetime import datetime
from config.db import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    motDePasseHash = Column(String(255), nullable=False)
    nom = Column(String(100))
    telephone = Column(String(20))
    avatarUrl = Column(String(255))
    bio = Column(String(500))
    professionnel = Column(Boolean, default=False)
    dateCreation = Column(DateTime, default=datetime.utcnow)
