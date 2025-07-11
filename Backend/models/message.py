from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
import uuid
from datetime import datetime
from config.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expediteurId = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    destinataireId = Column(String(36), ForeignKey("utilisateurs.id"), nullable=False)
    contenu = Column(String(2000), nullable=False)
    dateEnvoi = Column(DateTime, default=datetime.utcnow)
    lu = Column(Boolean, default=False)
