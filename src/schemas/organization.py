from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    name: str
    description: str
    city: str
    location: str


class OrganizationAdd(BaseModel):
    name: str
    description: str
    city: str
    location: str


class OrganizationToDateBase(OrganizationAdd):
    user_id: int


class OrganizationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    city: str | None = None
    location: str | None = None
