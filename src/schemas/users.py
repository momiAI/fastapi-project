from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    hash_password: str
    last_name: str
    first_name: str
    phone_number: str
    role: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserIncludeId(BaseModel):
    email: EmailStr
    hash_password: str
    last_name: str
    first_name: str
    phone_number: str
    role: int


class UserAdd(BaseModel):
    email: EmailStr
    password: str
    last_name: str
    first_name: str
    phone_number: str

