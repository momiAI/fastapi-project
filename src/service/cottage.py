import logging

from fastapi import UploadFile
from src.repositories.utils import upload_image
from src.schemas.cottage import CottageAdd, CottageToDateBase, CottageUpdate, CottageUpdateToDateBase
from src.schemas.facilities import AsociationFacilitiesCottage
from src.schemas.images import AsociationImagesCottage, ImageAdd
from src.service.base import BaseService
from src.tasks.tasks_storage import resize_image
from src.utis.exception import FacilitiesNotFound, IncorrectData, IncorrectDataCottage, ObjectNotFound,CottageNotFound,OrganizationNotFound, UserHasNotPermission
from src.route.dependency import HomePagination, SerchNotBook, UserIdDep


class CottageService(BaseService):

    async def get_cottage(self,id_org: int, id_cott: int):
        try:
            return await self.db.cottage.get_one_or_none(id=id_cott, organization_id=id_org)
        except ObjectNotFound:
            logging.debug(f"Не удалось найти коттедж с id : {id_cott.cottage_id}")        
            raise CottageNotFound
 
    async def get_free_cottage(
        self,
        data: SerchNotBook,
        pag: HomePagination,
        id_org: int | None,
    ):
        return await self.db.cottage.get_free_cottage(id_org, data, pag)
    
    async def add_cottage(
        self,
        id_org: int,
        data: CottageAdd 
    ):
        data_update = CottageToDateBase(organization_id=id_org, **data.model_dump())
        try: 
            cottage = await self.db.cottage.insert_to_database(data_update)
        except IncorrectData:
            raise OrganizationNotFound
        except IncorrectDataCottage:
            raise IncorrectDataCottage
        try:
            await self.db.asociatfacilcott.insert_to_database_bulk(
                [
                    AsociationFacilitiesCottage(id_cottage=cottage.id, id_facilities=i)
                    for i in data.facilities_ids
                ]
            )
        except IncorrectData:
            raise FacilitiesNotFound
        await self.db.commit()
        return cottage
            
    async def update_cottage(
        self,
        id_org: int,
        id_cott: int,
        id_user: UserIdDep,
        data: CottageUpdate
    ):
        verify = await self.db.organization.get_access_user_by_org(
            id_org=id_org, id_user=id_user
        )
        if not verify:
            logging.warning(f"Пользователь с {id_user=} попытался обновить организацию не пренадлежащую ему")
            raise UserHasNotPermission
        try:
            cottage = await self.db.cottage.patch_object(id_cott, CottageUpdateToDateBase(**data.model_dump(exclude_unset=True)))
        except IncorrectData:
            raise IncorrectDataCottage
        except ObjectNotFound:
            logging.debug(f"Не удалось найти коттедж с id : {data.cottage_id}")
            raise CottageNotFound

        if data.facilities_ids:
            try:
                await self.db.asociatfacilcott.patch_facilities(id_cottage = id_cott, data=data.facilities_ids)
            except ObjectNotFound:
                raise FacilitiesNotFound

        await self.db.session.commit()

        return cottage

    async def add_img_cottage(self,id_cott: int, images: UploadFile):
        img_stmt = await self.db.images.insert_to_database(
            ImageAdd(name_img=str(id_cott) + str(images.filename))
        )
        await self.db.asociatimagecottage.insert_to_database(
            AsociationImagesCottage(id_img=img_stmt.id, id_cottage=id_cott)
        )
        path = upload_image(images.filename, images.file, id_cott)
        logging.info("Начинаю обрабатывать изображения")
        resize_image.delay(path)
        logging.info("Закончил обрабатывать изображения")
        await self.db.session.commit()