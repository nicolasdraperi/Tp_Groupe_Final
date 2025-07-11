from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime

from models.message import Message
from schemas.message import MessageCreate

def envoyer_message(db: Session, message_data: MessageCreate, expediteur_id: str):
    nouveau_message = Message(
        id=str(uuid.uuid4()),
        expediteurId=expediteur_id,
        destinataireId=message_data.destinataireId,
        contenu=message_data.contenu,
        dateEnvoi=datetime.utcnow(),
        lu=False
    )
    db.add(nouveau_message)
    db.commit()
    db.refresh(nouveau_message)
    return nouveau_message

def lister_messages_recus(db: Session, utilisateur_id: str):
    return db.query(Message).filter(Message.destinataireId == utilisateur_id).all()

def lister_messages_envoyes(db: Session, utilisateur_id: str):
    return db.query(Message).filter(Message.expediteurId == utilisateur_id).all()

def marquer_comme_lu(db: Session, message_id: str, utilisateur_id: str):
    message = db.query(Message).filter(Message.id == message_id, Message.destinataireId == utilisateur_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message non trouvé ou accès interdit."
        )
    message.lu = True
    db.commit()
    db.refresh(message)
    return message
