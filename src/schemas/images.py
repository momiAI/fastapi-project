from pydantic import BaseModel


class Image(BaseModel):
    id : int
    name_img : str

class AsociationImagesCottage(BaseModel):
    id_img : int
    id_cottage : int