from pwdlib import PasswordHash
from fastapi import APIRouter,Body
from src.database import async_session_maker
from src.schemas.users import UserAdd,User
from src.repositories.users import UserRepository

route = APIRouter(prefix="/auth", tags=["Авторизация и Аутенфикация"])
hashed_set = PasswordHash.recommended()





@route.post("/register",summary="Регистрация пользователя")
async def register_user(data_user : UserAdd = Body(openapi_examples= {"1" : {"summary" : "Пользователь", "value" : {
    "email" : "test@example.ru",
    "password" : "password",
    "last_name" : "User",
    "first_name" : "Last",
    "phone_number" : "+7323889911"
}}})):
    data_user_update = User(email=data_user.email, 
                        hash_password= hashed_set.hash(data_user.password),
                        last_name=data_user.last_name, 
                        first_name= data_user.first_name, 
                        phone_number=data_user.phone_number) 
    async with async_session_maker() as session:
        result = await UserRepository(session).register(data_user_update.model_dump())
        await session.commit()
        return(result)