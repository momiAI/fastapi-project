from fastapi import APIRouter, Body
from src.route.dependency import DbDep
from src.schemas.facilities import FacilitiesCottageAdd
from src.route.dependency import SuperUserDep
from src.service.facilities import FacilitiesService
route = APIRouter(prefix="/facilitiec", tags=["Удобвства для коттеджей"])


@route.get("/cottage/all", summary="Получить все удобства коттеджей")
async def get_all_facilitiec_cottage(db: DbDep):
    return await FacilitiesService(db).get_all_facilitiec_cottage()


@route.post("/cottage/add", summary="Добавить удобство для коттеджей")
async def add_facilitiec_cottage(
    db: DbDep,
    user_check : SuperUserDep,
    data: FacilitiesCottageAdd = Body(
        openapi_examples={"1": {"summary": "Интернет", "value": {"title": "Интернет"}}}
    )
):
    result = await FacilitiesService(db).add_facilitiec_cottage(data)
    await db.commit()
    return {"message": "OK", "data": result}
