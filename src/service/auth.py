import jwt
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash
from src.config import settings
from src.schemas.users import UserIncludeId
class AuthService: 
    hashed_set = PasswordHash.recommended()


    def convert_data(self,email, hpassword,last_name,first_name, phone_number):
        user = UserIncludeId(email=email, 
                             hash_password=self.hash_password.hash(password),   
                             last_name=last_name,
                             first_name=first_name,
                             phone_number=phone_number)


    def create_access_token(self,data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def verify_password(self,plain_password, hashed_password):
        return self.hashed_set.verify(plain_password, hashed_password)
