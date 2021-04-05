import pytest 
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_sethandle_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.data import users
from src.other import clear_v1

def test_user_profile_setname_valid():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_name_first = 'mitchel'
    new_name_last = 'johnson'

    user_profile_setname_v1(new_token_1, new_name_first, new_name_last)

    for user in users:
        if user['token'] == new_token_1:
            user_info = {}
            user_info = user

    assert user_info['name_first'] == new_name_first and user_info['name_last'] == new_name_last

def test_name_first_too_short():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_name_first_short = 'm'
    new_name_last = 'johnson'

    with pytest.raises(InputError):
        user_profile_setname_v1(new_token_1, new_name_first_short, new_name_last)

def test_name_first_too_long():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_name_first_long = 'm' * 52
    new_name_last = 'johnson'

    with pytest.raises(InputError):
        user_profile_setname_v1(new_token_1, new_name_first_long, new_name_last)

def test_name_last_too_short():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_name_first = 'mitchel'
    new_name_last_short = 'j'

    with pytest.raises(InputError):
        user_profile_setname_v1(new_token_1, new_name_first, new_name_last_short)

def test_name_last_too_long():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_name_first = 'mitchel'
    new_name_last_long = 'j' * 52

    with pytest.raises(InputError):
        user_profile_setname_v1(new_token_1, new_name_first, new_name_last_long)