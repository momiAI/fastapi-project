from pydantic import BaseModel



class HomePUT(BaseModel):
    id : int
    title : str
    city : str
    street : str | None = None
    number_house : str | None = None
    square : int | None = None 
    price : int 
    description : str
    number : str
    rooms : int

class HomePATCH(BaseModel):
    id : int | None = None
    title : str | None = None
    city : str | None = None 
    street : str | None = None
    number_house : str | None = None
    square : int | None = None 
    price : int  | None = None
    description : str | None = None
    number : str | None = None
    rooms : int | None = None
