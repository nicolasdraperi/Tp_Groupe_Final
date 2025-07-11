from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageBase(BaseModel):
    contenu: str

class MessageCreate(MessageBase):
    expediteurId: str
    destinataireId: str

class MessageOut(MessageBase):
    id: str
    expediteurId: str
    destinataireId: str
    dateEnvoi: datetime
    lu: bool

    model_config = ConfigDict(from_attributes=True)
