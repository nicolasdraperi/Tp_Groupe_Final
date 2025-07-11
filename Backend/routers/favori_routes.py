from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import favori as schemas
from services import favori_service
from models.utilisateur import Utilisateur
from config.db import get_db
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.FavoriOut)
def ajouter_favori_endpoint(
    favori: schemas.FavoriCreate,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return favori_service.ajouter_favori(db, favori, utilisateur.id)

@router.delete("/{annonce_id}")
def supprimer_favori_endpoint(
    annonce_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    favori_service.supprimer_favori(db, annonce_id, utilisateur.id)
    return {"detail": "Favori supprimé."}

@router.get("/", response_model=List[schemas.FavoriOut])
def lister_favoris_endpoint(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return favori_service.lister_favoris(db, utilisateur.id)
