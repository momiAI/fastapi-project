import jwt
from fastapi import HTTPException
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash
from src.config import settings
from src.schemas.users import UserIncludeId
from src.config import settings
class AuthService: 
    hashed_set = PasswordHash.recommended()


    def convert_data(self,data_user):
        user = UserIncludeId(email=data_user.get("email"), 
                             hash_password=self.hashed_set.hash(data_user.get("password")),   
                             last_name=data_user.get("last_name"),
                             first_name=data_user.get("first_name"),
                             phone_number=data_user.get("phone_number"))
        return user


    def create_access_token(self,data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def decode_token(self, token):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок токена истек")



    def verify_password(self,plain_password, hashed_password):
        return self.hashed_set.verify(plain_password, hashed_password)

authservice = AuthService()