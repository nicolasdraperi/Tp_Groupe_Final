import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services import utilisateur_service
from schemas.utilisateur import UtilisateurCreate


@pytest.fixture
def fake_user():
    class FakeUser:
        def __init__(self, id, email, motDePasseHash):
            self.id = id
            self.email = email
            self.motDePasseHash = motDePasseHash
            self.nom = "Test"
            self.telephone = "0601020304"
            self.avatarUrl = None
            self.bio = None
            self.professionnel = False
            self.dateCreation = None
    return FakeUser

def test_creer_utilisateur_success(monkeypatch):
    db = MagicMock()
    db.query().filter().first.return_value = None
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    user_data = UtilisateurCreate(
        email="test@example.com",
        motDePasse="secret",
        nom="Test",
        telephone="0601020304",
        avatarUrl=None,
        bio=None,
        professionnel=False
    )

    result = utilisateur_service.creer_utilisateur(db, user_data)
    assert result.email == "test@example.com"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_creer_utilisateur_email_existe():
    db = MagicMock()
    db.query().filter().first.return_value = "already_exists"

    user_data = UtilisateurCreate(
        email="test@example.com",
        motDePasse="secret",
        nom="Test",
        telephone="0601020304",
        avatarUrl=None,
        bio=None,
        professionnel=False
    )

    with pytest.raises(HTTPException) as exc:
        utilisateur_service.creer_utilisateur(db, user_data)
    assert exc.value.status_code == 400

def test_authentifier_utilisateur_success(fake_user, monkeypatch):
    hashed_password = utilisateur_service.hash_password("secret")
    user_instance = fake_user("uuid123", "test@example.com", hashed_password)

    db = MagicMock()
    db.query().filter().first.return_value = user_instance

    result = utilisateur_service.authentifier_utilisateur(db, "test@example.com", "secret")
    assert result.email == "test@example.com"

def test_authentifier_utilisateur_wrong_password(fake_user):
    hashed_password = utilisateur_service.hash_password("correct")
    user_instance = fake_user("uuid123", "test@example.com", hashed_password)

    db = MagicMock()
    db.query().filter().first.return_value = user_instance

    with pytest.raises(HTTPException) as exc:
        utilisateur_service.authentifier_utilisateur(db, "test@example.com", "wrongpassword")
    assert exc.value.status_code == 401

def test_obtenir_utilisateur_par_id_success(fake_user):
    user_instance = fake_user("uuid123", "test@example.com", "hash")

    db = MagicMock()
    db.query().filter().first.return_value = user_instance

    result = utilisateur_service.obtenir_utilisateur_par_id(db, "uuid123")
    assert result.email == "test@example.com"

def test_obtenir_utilisateur_par_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        utilisateur_service.obtenir_utilisateur_par_id(db, "uuid123")
    assert exc.value.status_code == 404

def test_mettre_a_jour_utilisateur(monkeypatch, fake_user):
    user_instance = fake_user("uuid123", "test@example.com", "hash")

    db = MagicMock()
    db.query().filter().first.return_value = user_instance

    monkeypatch.setattr(utilisateur_service, "obtenir_utilisateur_par_id", lambda db, id: user_instance)

    updates = {"nom": "Nouveau Nom"}
    result = utilisateur_service.mettre_a_jour_utilisateur(db, "uuid123", updates)
    assert result.nom == "Nouveau Nom"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
