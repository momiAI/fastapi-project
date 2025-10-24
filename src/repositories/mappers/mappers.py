from src.repositories.mappers.base import DataMapper

from src.models.users import UsersModel
from src.models.house import HouseModel
from src.models.cottage import CottageModel
from src.models.booking import BookingModel
from src.models.organization import OrganizationModel
from src.models.facilitiec import FacilitiesCottageModel,AsociationFacilitiesCottageModel

from src.schemas.users import User
from src.schemas.house import House
from src.schemas.cottage import Cottage
from src.schemas.booking import Booking
from src.schemas.organization import Organization
from src.schemas.facilities import FacilitiesCottage,AsociationFacilitiesCottage

class UserMapper(DataMapper):
    db_model = UsersModel
    db_schema = User

class HouseMapper(DataMapper):
    db_model = HouseModel
    db_schema = House

class CottageMapper(DataMapper):
    db_model = CottageModel
    db_schema = Cottage

class BookingMapper(DataMapper):
    db_model = BookingModel
    db_schema = Booking

class OrganizationMapper(DataMapper):
    db_model = OrganizationModel
    db_schema = Organization

class FacilitiesCottageMapper(DataMapper):
    db_model = FacilitiesCottageModel
    db_schema = FacilitiesCottage

class AsociationFacilitiesCottageMapper(DataMapper):
    db_model = AsociationFacilitiesCottageModel
    db_schema = AsociationFacilitiesCottage