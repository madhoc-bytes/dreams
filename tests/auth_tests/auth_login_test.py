import pytest 
from src.auth import auth_login_v1, auth_register_v1
from src.error import InputError
from src.data import users
from src.other import clear_v1


def test_auth_login_valid():
    clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    new_user_id = auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']

    assert auth_login_v1(valid_email, valid_password) == new_user_id

def test_valid_email():
    clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    invalid_email = 'abc.com'
    auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']

    with pytest.raises(InputError):
        auth_login_v1(invalid_email, valid_password)

def test_wrong_email():
    clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    wrong_email = 'def@def.com'
    auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']

    with pytest.raises(InputError):
        auth_login_v1(wrong_email, valid_password)
    
def test_wrong_password():
    clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    wrong_password = 'helloWorld1'
    auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']

    with pytest.raises(InputError):
        auth_login_v1(valid_email, wrong_password)


        
        


