import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services import annonce_service
from schemas.annonce import AnnonceCreate, AnnonceUpdate

@pytest.fixture
def fake_annonce():
    class FakeAnnonce:
        def __init__(self, id, utilisateurId):
            self.id = id
            self.utilisateurId = utilisateurId
            self.titre = "Test"
            self.description = "Description"
            self.prix = 10.0
            self.categorie = "Categorie"
            self.lieu = "Paris"
            self.latitude = None
            self.longitude = None
            self.active = True
        def __setattr__(self, key, value):
            super().__setattr__(key, value)
    return FakeAnnonce

def test_creer_annonce_success():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    data = AnnonceCreate(
        titre="Test",
        description="Desc",
        prix=10.0,
        categorie="Cat",
        lieu="Paris",
        utilisateurId="user-id",
        latitude=None,
        longitude=None
    )

    result = annonce_service.creer_annonce(db, data, "user-id")
    assert result.titre == "Test"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_obtenir_annonce_par_id_success(fake_annonce):
    db = MagicMock()
    db.query().filter().first.return_value = fake_annonce("annonce-id", "user-id")

    result = annonce_service.obtenir_annonce_par_id(db, "annonce-id")
    assert result.id == "annonce-id"

def test_obtenir_annonce_par_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        annonce_service.obtenir_annonce_par_id(db, "annonce-id")
    assert exc.value.status_code == 404

def test_lister_annonces():
    db = MagicMock()
    annonces_list = ["a1", "a2"]
    db.query().offset().limit().all.return_value = annonces_list

    result = annonce_service.lister_annonces(db)
    assert result == annonces_list

def test_mettre_a_jour_annonce_success(monkeypatch, fake_annonce):
    annonce_instance = fake_annonce("annonce-id", "user-id")
    db = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    monkeypatch.setattr(annonce_service, "obtenir_annonce_par_id", lambda db, id: annonce_instance)

    updates = AnnonceUpdate(
        titre="Nouveau titre",
        description=None,
        prix=None,
        categorie=None,
        lieu=None,
        active=True,
        latitude=None,
        longitude=None
    )

    result = annonce_service.mettre_a_jour_annonce(db, "annonce-id", updates, "user-id")
    assert result.titre == "Nouveau titre"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_mettre_a_jour_annonce_forbidden(monkeypatch, fake_annonce):
    annonce_instance = fake_annonce("annonce-id", "other-user-id")

    monkeypatch.setattr(annonce_service, "obtenir_annonce_par_id", lambda db, id: annonce_instance)

    db = MagicMock()
    updates = AnnonceUpdate(
        titre="Nouveau titre",
        description=None,
        prix=None,
        categorie=None,
        lieu=None,
        active=True,
        latitude=None,
        longitude=None
    )

    with pytest.raises(HTTPException) as exc:
        annonce_service.mettre_a_jour_annonce(db, "annonce-id", updates, "user-id")
    assert exc.value.status_code == 403

def test_supprimer_annonce_success(monkeypatch, fake_annonce):
    annonce_instance = fake_annonce("annonce-id", "user-id")
    db = MagicMock()
    db.delete = MagicMock()
    db.commit = MagicMock()

    monkeypatch.setattr(annonce_service, "obtenir_annonce_par_id", lambda db, id: annonce_instance)

    annonce_service.supprimer_annonce(db, "annonce-id", "user-id")
    db.delete.assert_called_once()
    db.commit.assert_called_once()

def test_supprimer_annonce_forbidden(monkeypatch, fake_annonce):
    annonce_instance = fake_annonce("annonce-id", "other-user-id")
    monkeypatch.setattr(annonce_service, "obtenir_annonce_par_id", lambda db, id: annonce_instance)

    db = MagicMock()

    with pytest.raises(HTTPException) as exc:
        annonce_service.supprimer_annonce(db, "annonce-id", "user-id")
    assert exc.value.status_code == 403
