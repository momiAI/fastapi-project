from pydantic import BaseModel

class Cottage(BaseModel):
    id : int
    organization_id : int
    name_house : str
    description : str
    people : int
    price : int
    
class CottageToDateBase(BaseModel):
    organization_id : int
    name_house : str
    description : str
    people : int
    price : int


class CottageAdd(BaseModel):
    name_house : str
    description : str
    people : int
    price : int
    facilities_ids : list[int] | None = None


class CottageUpdate(BaseModel):
    name_house : str | None = None
    description : str | None = None
    people : int | None = None
    price : int | None = None
    facilities_ids : list[int] | None = None
    
class CottageUpdateToDateBase(BaseModel):
    name_house : str | None = None
    description : str | None = None
    people : int | None = None
    price : int | None = None
