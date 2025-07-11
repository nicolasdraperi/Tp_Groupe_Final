from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    expediteurId = Column(String, ForeignKey("utilisateurs.id"), nullable=False)
    destinataireId = Column(String, ForeignKey("utilisateurs.id"), nullable=False)
    contenu = Column(String, nullable=False)
    dateEnvoi = Column(DateTime, default=datetime.utcnow)
    lu = Column(Boolean, default=False)
