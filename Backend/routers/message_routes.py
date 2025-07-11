from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import message as schemas
from services import message_service
from models.utilisateur import Utilisateur
from config.db import get_db
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.MessageOut)
def envoyer_message_endpoint(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return message_service.envoyer_message(db, message, utilisateur.id)

@router.get("/recus", response_model=List[schemas.MessageOut])
def lister_messages_recus_endpoint(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return message_service.lister_messages_recus(db, utilisateur.id)

@router.get("/envoyes", response_model=List[schemas.MessageOut])
def lister_messages_envoyes_endpoint(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return message_service.lister_messages_envoyes(db, utilisateur.id)

@router.put("/{message_id}/lu", response_model=schemas.MessageOut)
def marquer_message_lu_endpoint(
    message_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(get_current_user)
):
    return message_service.marquer_comme_lu(db, message_id, utilisateur.id)
