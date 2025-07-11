from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db import Base, engine

# Importer tous les modèles pour les migrations/tables
import models.utilisateur
import models.annonce
import models.message
import models.favori
import models.paiement
import models.alerte

# Importer tes routers
from routers import (
    utilisateur_routes,
    annonce_routes,
    message_routes,
    favori_routes,
    paiement_routes
)


print("📦 Création des tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès")

app = FastAPI(title="API Vendre Facile")

# Middleware CORS pour autoriser le front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adapte si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure tes routers

app.include_router(utilisateur_routes.router, prefix="/api/utilisateurs", tags=["Utilisateurs"])
app.include_router(annonce_routes.router, prefix="/api/annonces", tags=["Annonces"])
app.include_router(message_routes.router, prefix="/api/messages", tags=["Messages"])
app.include_router(favori_routes.router, prefix="/api/favoris", tags=["Favoris"])
app.include_router(paiement_routes.router, prefix="/api/paiements", tags=["Paiements"])
'''
app.include_router(alerte_routes.router, prefix="/api/alertes", tags=["Alertes"])
'''