
from fastapi import APIRouter,Body,HTTPException,Response
from src.service.auth import AuthService 
from src.database import async_session_maker
from src.schemas.users import UserAdd,UserIncludeId,UserLogin
from src.repositories.users import UserRepository

route = APIRouter(prefix="/auth", tags=["Авторизация и Аутенфикация"])



@route.post("/register",summary="Регистрация пользователя")
async def register_user(data_user : UserAdd = Body(openapi_examples= {"1" : {"summary" : "Пользователь", "value" : {
    "email" : "test@example.ru",
    "password" : "password",
    "last_name" : "User",
    "first_name" : "Last",
    "phone_number" : "+7323889911"
}}})):
    data_user_update = UserIncludeId(email=data_user.email, 
                      hash_password= AuthService.hashed_set.hash(data_user.password),
                      last_name=data_user.last_name, 
                      first_name= data_user.first_name, 
                      phone_number=data_user.phone_number) 
    async with async_session_maker() as session:
        result = await UserRepository(session).register(data_user_update.model_dump())
        await session.commit()
        return(result)
    

@route.post("/login", summary="Аутенфикация пользователя")
async def login_user(response : Response,data_user : UserLogin = Body(openapi_examples= {"1" : {"summary" : "Пользователь1", "value" : {
    "email" : "vlad@ya.ru",
    "password" : "qwerty"
}}})):

    async with async_session_maker() as session:
        user = await UserRepository(session).get_one_or_none(email = data_user.email)
        if user is None or AuthService.verify_password(data_user.password, user.hash_password) is False:
            raise HTTPException(status_code=401, detail="Проверьте корректность вводимых данных!")
        acess_token = AuthService.create_access_token({"user_id" : user.id})
        response.set_cookie("access_token", acess_token)
        return {"access_token" : acess_token}