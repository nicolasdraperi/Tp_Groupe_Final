import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from services import favori_service
from schemas.favori import FavoriCreate

@pytest.fixture
def fake_favori():
    class FakeFavori:
        def __init__(self, id, utilisateurId, annonceId):
            self.id = id
            self.utilisateurId = utilisateurId
            self.annonceId = annonceId
    return FakeFavori

def test_ajouter_favori_success():
    db = MagicMock()
    db.query().filter().first.return_value = None
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    favori_data = FavoriCreate(
    annonceId="annonce-id",
    utilisateurId="user-id"
)

    result = favori_service.ajouter_favori(db, favori_data, "user-id")

    assert result.annonceId == "annonce-id"
    assert result.utilisateurId == "user-id"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_ajouter_favori_already_exists():
    db = MagicMock()
    db.query().filter().first.return_value = "existing"

    favori_data = FavoriCreate(
    annonceId="annonce-id",
    utilisateurId="user-id"
)


    with pytest.raises(HTTPException) as exc:
        favori_service.ajouter_favori(db, favori_data, "user-id")

    assert exc.value.status_code == 400

def test_supprimer_favori_success(fake_favori):
    favori_instance = fake_favori("fav-id", "user-id", "annonce-id")
    db = MagicMock()
    db.query().filter().first.return_value = favori_instance
    db.delete = MagicMock()
    db.commit = MagicMock()

    favori_service.supprimer_favori(db, "annonce-id", "user-id")
    db.delete.assert_called_once_with(favori_instance)
    db.commit.assert_called_once()

def test_supprimer_favori_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        favori_service.supprimer_favori(db, "annonce-id", "user-id")

    assert exc.value.status_code == 404

def test_lister_favoris():
    db = MagicMock()
    favoris_list = ["f1", "f2"]
    db.query().filter().all.return_value = favoris_list

    result = favori_service.lister_favoris(db, "user-id")
    assert result == favoris_list
