from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email : EmailStr
    hash_password : str
    last_name : str
    first_name : str
    phone_number : str

class UserAdd(BaseModel):
    email : EmailStr
    password : str
    last_name : str
    first_name : str
    phone_number : str