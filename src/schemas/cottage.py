from pydantic import BaseModel

class Cottage(BaseModel):
    id : int
    organization_id : int
    name_house : str
    description : str
    people : int
    price : int
    animals : bool

class CottageAdd(BaseModel):
    name_house : str
    description : str
    people : int
    price : int
    animals : bool

class CottageUpdate(BaseModel):
    name_house : str | None = None
    description : str | None = None
    people : int | None = None
    price : int | None = None
    animals : bool | None = None
