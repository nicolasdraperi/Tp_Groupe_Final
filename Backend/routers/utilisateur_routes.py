from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import utilisateur as schemas
from services import utilisateur_service
from config.db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UtilisateurOut)
def creer_utilisateur_endpoint(user: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    return utilisateur_service.creer_utilisateur(db, user)

@router.post("/login", response_model=schemas.TokenResponse)
def login_utilisateur_endpoint(credentials: schemas.ConnexionRequest, db: Session = Depends(get_db)):
    return utilisateur_service.connexion_utilisateur(db, credentials.email, credentials.motDePasse)
