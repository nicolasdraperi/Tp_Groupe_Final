from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import alerte as schemas
from services import alerte_service
from models.utilisateur import Utilisateur
from config.db import get_db
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.AlerteOut)
def creer_alerte_endpoint(
    alerte: schemas.AlerteCreate,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return alerte_service.creer_alerte(db, alerte, utilisateur.id)

@router.get("/", response_model=List[schemas.AlerteOut])
def lister_alertes_endpoint(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return alerte_service.lister_alertes(db, utilisateur.id)

@router.put("/{alerte_id}/lue", response_model=schemas.AlerteOut)
def marquer_alerte_lue_endpoint(
    alerte_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return alerte_service.marquer_alerte_comme_lue(db, alerte_id, utilisateur.id)
