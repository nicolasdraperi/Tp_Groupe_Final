from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime

from models.paiement import Paiement
from schemas.paiement import PaiementCreate

def creer_paiement(db: Session, paiement_data: PaiementCreate, utilisateur_id: str):
    nouveau_paiement = Paiement(
        id=str(uuid.uuid4()),
        utilisateurId=utilisateur_id,
        annonceId=paiement_data.annonceId,
        montant=paiement_data.montant,
        statut="en_attente",
        dateCreation=datetime.utcnow()
    )
    db.add(nouveau_paiement)
    db.commit()
    db.refresh(nouveau_paiement)
    return nouveau_paiement

def obtenir_paiement_par_id(db: Session, paiement_id: str, utilisateur_id: str):
    paiement = db.query(Paiement).filter(
        Paiement.id == paiement_id,
        Paiement.utilisateurId == utilisateur_id
    ).first()
    if not paiement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paiement non trouvé."
        )
    return paiement

def lister_paiements_utilisateur(db: Session, utilisateur_id: str):
    return db.query(Paiement).filter(Paiement.utilisateurId == utilisateur_id).all()

def mettre_a_jour_statut_paiement(db: Session, paiement_id: str, nouveau_statut: str, utilisateur_id: str):
    paiement = obtenir_paiement_par_id(db, paiement_id, utilisateur_id)
    paiement.statut = nouveau_statut
    db.commit()
    db.refresh(paiement)
    return paiement
