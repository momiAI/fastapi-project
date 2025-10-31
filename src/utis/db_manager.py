from src.repositories.house import HouseRepository
from src.repositories.users import UserRepository
from src.repositories.images import ImagesRepository,AsociationImagesCottageRepository
from src.repositories.cottage import CottageRepository
from src.repositories.organization import OrganizationRepository
from src.repositories.booking import BookingRepository
from src.repositories.facilitiec import FacilitiesCottageRepository,AsociationFacilitiesCottageRepository




class DbManager:

    def __init__(self,session_factory):
        self.session_factory = session_factory

    async def __aenter__ (self):
        self.session = self.session_factory()

        self.house = HouseRepository(self.session)
        self.user = UserRepository(self.session)
        self.cottage = CottageRepository(self.session)
        self.images = ImagesRepository(self.session)
        self.organization = OrganizationRepository(self.session)
        self.booking = BookingRepository(self.session)
        self.facilcott = FacilitiesCottageRepository(self.session)
        self.asociatfacilcott = AsociationFacilitiesCottageRepository(self.session)
        self.asociatimagecottage = AsociationImagesCottageRepository(self.session)
        
        return self
        
    async def __aexit__ (self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
       await self.session.commit()