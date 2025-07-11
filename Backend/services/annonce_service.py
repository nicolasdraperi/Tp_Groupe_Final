from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime, UTC

from models.annonce import Annonce
from schemas.annonce import AnnonceCreate, AnnonceUpdate

def creer_annonce(db: Session, annonce_data: AnnonceCreate, utilisateur_id: str):
    nouvelle_annonce = Annonce(
        id=str(uuid.uuid4()),
        titre=annonce_data.titre,
        description=annonce_data.description,
        prix=annonce_data.prix,
        categorie=annonce_data.categorie,
        lieu=annonce_data.lieu,
        dateCreation=datetime.now(UTC),
        utilisateurId=utilisateur_id,
        active=True,
        latitude=annonce_data.latitude,
        longitude=annonce_data.longitude
    )
    db.add(nouvelle_annonce)
    db.commit()
    db.refresh(nouvelle_annonce)
    return nouvelle_annonce


def obtenir_annonce_par_id(db: Session, annonce_id: str):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce non trouvée."
        )
    return annonce


def lister_annonces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Annonce).offset(skip).limit(limit).all()


def mettre_a_jour_annonce(db: Session, annonce_id: str, updates: AnnonceUpdate, utilisateur_id: str):
    annonce = obtenir_annonce_par_id(db, annonce_id)

    if annonce.utilisateurId != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que vos propres annonces."
        )

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(annonce, key, value)

    db.commit()
    db.refresh(annonce)
    return annonce


def supprimer_annonce(db: Session, annonce_id: str, utilisateur_id: str):
    annonce = obtenir_annonce_par_id(db, annonce_id)

    if annonce.utilisateurId != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez supprimer que vos propres annonces."
        )

    db.delete(annonce)
    db.commit()
