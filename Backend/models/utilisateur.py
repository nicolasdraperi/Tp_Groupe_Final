from sqlalchemy import Column, String, Boolean, DateTime
import uuid
from datetime import datetime
from config.db import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    motDePasseHash = Column(String, nullable=False)
    nom = Column(String)
    telephone = Column(String)
    avatarUrl = Column(String)
    bio = Column(String)
    professionnel = Column(Boolean, default=False)
    dateCreation = Column(DateTime, default=datetime.utcnow)
