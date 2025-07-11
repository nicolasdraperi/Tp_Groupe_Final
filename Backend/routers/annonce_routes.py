from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import annonce as schemas
from services import annonce_service
from models.utilisateur import Utilisateur
from config.db import get_db
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.AnnonceOut)
def creer_annonce_endpoint(
    annonce: schemas.AnnonceCreate,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return annonce_service.creer_annonce(db, annonce, utilisateur.id)

@router.get("/", response_model=List[schemas.AnnonceOut])
def lister_annonces_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return annonce_service.lister_annonces(db, skip=skip, limit=limit)

@router.get("/{annonce_id}", response_model=schemas.AnnonceOut)
def get_annonce_endpoint(annonce_id: str, db: Session = Depends(get_db)):
    return annonce_service.obtenir_annonce_par_id(db, annonce_id)

@router.put("/{annonce_id}", response_model=schemas.AnnonceOut)
def update_annonce_endpoint(
    annonce_id: str,
    updates: schemas.AnnonceBase,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return annonce_service.mettre_a_jour_annonce(db, annonce_id, updates, utilisateur.id)

@router.delete("/{annonce_id}")
def delete_annonce_endpoint(
    annonce_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    annonce_service.supprimer_annonce(db, annonce_id, utilisateur.id)
    return {"detail": "Annonce supprimée."}
