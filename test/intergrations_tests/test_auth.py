from src.service.auth import AuthService

def test_check_register_and_auth():
    data = {"user_id" : 1 , "user_role" : 1 }
    
    create_jwt_token = AuthService().create_access_token(data)

    assert create_jwt_token
    assert isinstance(create_jwt_token, str) 

    encode_token = AuthService().decode_token(create_jwt_token)
    assert encode_token.get("user_id") == data["user_id"]
