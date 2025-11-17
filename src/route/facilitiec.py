from fastapi import APIRouter, Body
from src.route.dependency import DbDep
from src.schemas.facilities import FacilitiesCottageAdd

route = APIRouter(prefix="/facilitiec", tags=["Удобвства для коттеджей"])


@route.get("/cottage/all", summary="Получить все удобства коттеджей")
async def get_all_facilitiec_cottage(db: DbDep):
    return await db.facilcott.get_all()


@route.post("/cottage/add", summary="Добавить удобство для коттеджей")
async def add_facilitiec_cottage(
    db: DbDep,
    data: FacilitiesCottageAdd = Body(
        openapi_examples={"1": {"summary": "Интернет", "value": {"title": "Интернет"}}}
    ),
):
    result = await db.facilcott.insert_to_database(data)
    await db.commit()
    return {"message": "OK", "data": result}
