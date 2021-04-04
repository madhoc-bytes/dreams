import pytest 
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v2
from src.error import InputError
from src.data import users
from src.other import clear_v1


def test_auth_logout_valid():
    clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    auth_register_v2(valid_email, valid_password, valid_first_name, valid_last_name)
    
    login_return = auth_login_v2(valid_email, valid_password)
    new_token = login_return['token']

    print(f"{login_return['token']}")

    assert auth_logout_v2(new_token) == {'is_success': True}