from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

class PaiementBase(BaseModel):
    utilisateurId: str
    annonceId: str
    montant: Decimal
    statut: str

class PaiementCreate(PaiementBase):
    pass

class PaiementOut(PaiementBase):
    id: str
    dateCreation: datetime

    model_config = ConfigDict(from_attributes=True)
