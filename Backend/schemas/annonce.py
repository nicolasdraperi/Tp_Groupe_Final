from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime

class AnnonceBase(BaseModel):
    titre: str
    description: Optional[str] = None
    prix: Optional[Decimal] = None
    categorie: Optional[str] = None
    lieu: Optional[str] = None
    active: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AnnonceCreate(AnnonceBase):
    utilisateurId: str

class AnnonceUpdate(AnnonceBase):
    pass

class AnnonceOut(AnnonceBase):
    id: str
    utilisateurId: str
    dateCreation: datetime

    model_config = ConfigDict(from_attributes=True)
