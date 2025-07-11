from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import paiement as schemas
from services import paiement_service
from models.utilisateur import Utilisateur
from config.db import get_db
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.PaiementOut)
def creer_paiement_endpoint(
    paiement: schemas.PaiementCreate,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return paiement_service.creer_paiement(db, paiement, utilisateur.id)

@router.get("/{paiement_id}", response_model=schemas.PaiementOut)
def obtenir_paiement_endpoint(
    paiement_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return paiement_service.obtenir_paiement_par_id(db, paiement_id, utilisateur.id)

@router.get("/", response_model=List[schemas.PaiementOut])
def lister_paiements_endpoint(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return paiement_service.lister_paiements_utilisateur(db, utilisateur.id)

@router.put("/{paiement_id}/statut", response_model=schemas.PaiementOut)
def mettre_a_jour_statut_endpoint(
    paiement_id: str,
    nouveau_statut: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return paiement_service.mettre_a_jour_statut_paiement(db, paiement_id, nouveau_statut, utilisateur.id)
