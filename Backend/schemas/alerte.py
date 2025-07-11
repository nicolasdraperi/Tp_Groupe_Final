from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AlerteBase(BaseModel):
    utilisateurId: str
    message: str

class AlerteCreate(AlerteBase):
    pass

class AlerteOut(AlerteBase):
    id: str
    dateEnvoi: datetime
    lu: bool

    model_config = ConfigDict(from_attributes=True)
