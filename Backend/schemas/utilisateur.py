from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UtilisateurBase(BaseModel):
    email: EmailStr
    nom: str
    telephone: Optional[str] = None
    avatarUrl: Optional[str] = None
    bio: Optional[str] = None
    professionnel: bool = False

class UtilisateurCreate(UtilisateurBase):
    motDePasse: str

class UtilisateurOut(UtilisateurBase):
    id: str
    dateCreation: datetime

    class Config:
        orm_mode = True

class ConnexionRequest(BaseModel):
    email: EmailStr
    motDePasse: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
