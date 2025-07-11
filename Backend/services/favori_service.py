from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid

from models.favori import Favori
from schemas.favori import FavoriCreate

def ajouter_favori(db: Session, favori_data: FavoriCreate, utilisateur_id: str):
    existing = db.query(Favori).filter(
        Favori.utilisateurId == utilisateur_id,
        Favori.annonceId == favori_data.annonceId
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Annonce déjà dans les favoris."
        )
    nouveau_favori = Favori(
        id=str(uuid.uuid4()),
        utilisateurId=utilisateur_id,
        annonceId=favori_data.annonceId
    )
    db.add(nouveau_favori)
    db.commit()
    db.refresh(nouveau_favori)
    return nouveau_favori

def supprimer_favori(db: Session, annonce_id: str, utilisateur_id: str):
    favori = db.query(Favori).filter(
        Favori.utilisateurId == utilisateur_id,
        Favori.annonceId == annonce_id
    ).first()
    if not favori:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favori non trouvé."
        )
    db.delete(favori)
    db.commit()

def lister_favoris(db: Session, utilisateur_id: str):
    return db.query(Favori).filter(Favori.utilisateurId == utilisateur_id).all()
