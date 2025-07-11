from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime

from models.alerte import Alerte
from schemas.alerte import AlerteCreate

def creer_alerte(db: Session, alerte_data: AlerteCreate, utilisateur_id: str):
    nouvelle_alerte = Alerte(
        id=str(uuid.uuid4()),
        utilisateurId=utilisateur_id,
        message=alerte_data.message,
        dateEnvoi=datetime.utcnow(),
        lu=False
    )
    db.add(nouvelle_alerte)
    db.commit()
    db.refresh(nouvelle_alerte)
    return nouvelle_alerte

def lister_alertes(db: Session, utilisateur_id: str):
    return db.query(Alerte).filter(Alerte.utilisateurId == utilisateur_id).all()

def marquer_alerte_comme_lue(db: Session, alerte_id: str, utilisateur_id: str):
    alerte = db.query(Alerte).filter(
        Alerte.id == alerte_id,
        Alerte.utilisateurId == utilisateur_id
    ).first()
    if not alerte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerte non trouvée."
        )
    alerte.lu = True
    db.commit()
    db.refresh(alerte)
    return alerte
