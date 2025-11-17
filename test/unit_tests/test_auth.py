from src.service.auth import AuthService


def test_create_acess_token():
    data = {"user_id": 1, "user_role": 1}

    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)
