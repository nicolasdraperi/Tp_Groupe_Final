from sqlalchemy.orm import Session
from passlib.context import CryptContext
import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from models.utilisateur import Utilisateur
from schemas.utilisateur import UtilisateurCreate


SECRET_KEY = "supersecretpourlejwt"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def creer_utilisateur(db: Session, utilisateur_data: UtilisateurCreate):
    existing = db.query(Utilisateur).filter(Utilisateur.email == utilisateur_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà enregistré."
        )
    
    hashed_pwd = hash_password(utilisateur_data.motDePasse)
    nouvel_utilisateur = Utilisateur(
        id=str(uuid.uuid4()),
        email=utilisateur_data.email,
        motDePasseHash=hashed_pwd,
        nom=utilisateur_data.nom,
        telephone=utilisateur_data.telephone,
        avatarUrl=utilisateur_data.avatarUrl,
        bio=utilisateur_data.bio,
        professionnel=utilisateur_data.professionnel,
        dateCreation=datetime.utcnow()
    )
    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)
    return nouvel_utilisateur


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authentifier_utilisateur(db: Session, email: str, password: str):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if not utilisateur or not verify_password(password, utilisateur.motDePasseHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides."
        )
    return utilisateur


def connexion_utilisateur(db: Session, email: str, password: str):
    utilisateur = authentifier_utilisateur(db, email, password)
    token_data = {
        "sub": utilisateur.id,
        "email": utilisateur.email,
    }
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
    

def obtenir_utilisateur_par_id(db: Session, utilisateur_id: str):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé."
        )
    return utilisateur


def mettre_a_jour_utilisateur(db: Session, utilisateur_id: str, updates: dict):
    utilisateur = obtenir_utilisateur_par_id(db, utilisateur_id)
    
    for key, value in updates.items():
        if hasattr(utilisateur, key) and value is not None:
            setattr(utilisateur, key, value)
    
    db.commit()
    db.refresh(utilisateur)
    return utilisateur
