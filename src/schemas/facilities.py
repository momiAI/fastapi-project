from pydantic import BaseModel


class FacilitiesCottage(BaseModel):
    id : int
    title : str


class FacilitiesCottageAdd(BaseModel):
    title : str


class AsociationFacilitiesCottage(BaseModel):
    id_facilities : int
    id_cottage : int