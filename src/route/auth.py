
from fastapi import APIRouter,Body,HTTPException,Response
from src.service.auth import authservice 
from src.route.dependency import UserIdDep, DbDep
from src.schemas.users import UserAdd,UserLogin


route = APIRouter(prefix="/auth", tags=["Авторизация и Аутенфикация"])



@route.post("/register",summary="Регистрация пользователя")
async def register_user(db : DbDep,data_user : UserAdd = Body(openapi_examples= {"1" : {"summary" : "Пользователь", "value" : {
    "email" : "test@example.ru",
    "password" : "password",
    "last_name" : "User",
    "first_name" : "Last",
    "phone_number" : "+7323889911"
}}})):
    data_user_update = authservice.convert_data(data_user.model_dump())
    result = await db.user.register(data_user_update.model_dump())
    await db.commit()
    return {"message" : "OK"}
    

@route.post("/login", summary="Аутенфикация пользователя")
async def login_user(db : DbDep,response : Response,data_user : UserLogin = Body(openapi_examples= {"1" : {"summary" : "Пользователь1", "value" : {
    "email" : "vlad@ya.ru",
    "password" : "qwerty"
}}})):
    user = await db.user.get_one_or_none(email = data_user.email)
    if user is None or authservice.verify_password(data_user.password, user.hash_password) is False:
        raise HTTPException(status_code=401, detail="Проверьте корректность вводимых данных!")
    acess_token = authservice.create_access_token({"user_id" : user.id})
    response.set_cookie("access_token", acess_token)
    return {"access_token" : acess_token}
    

@route.post("/logout", summary="Удаление куков")
async def logout_user(response : Response): 
    response.delete_cookie("access_token")
    return {"status" : "OK"}


@route.get("/get/me")
async def get_me(db : DbDep,user_id : UserIdDep):
    return await db.user.get_one_or_none(id = user_id)


#Добавить ручку на обновление с проверкой имеет ли авторизированный пользователь обновлять отель