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