from pydantic import BaseModel, ConfigDict

class FavoriBase(BaseModel):
    utilisateurId: str
    annonceId: str

class FavoriCreate(FavoriBase):
    pass

class FavoriOut(FavoriBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
