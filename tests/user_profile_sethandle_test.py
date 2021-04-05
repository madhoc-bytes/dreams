import pytest 
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_sethandle_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.data import users
from src.other import clear_v1

def test_user_set_handle_valid():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']

    new_handle = 'thisisnewhandle'

    user_profile_sethandle_v1(new_token_1, new_handle)

    for user in users:
        if user['token'] == new_token_1:
            user_info = user
        
    assert user_info['handle'] == new_handle

def test_new_handle_too_short():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_handle_short = 'h'

    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_token_1, new_handle_short)

def test_new_handle_too_long():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']
        
    new_handle_long = 'h' * 22

    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_token_1, new_handle_long)

def test_used_handle():

    clear_v1()

    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
        valid_email_1, 
        valid_password_1, 
        valid_first_name_1, 
        valid_last_name_1)['token']
    
    
    valid_email_2, valid_password_2 = 'abc@defg.com', 'helloWorld123!'
    valid_first_name_2, valid_last_name_2 = 'mitchel', 'johnson'
    new_token_2 = auth_register_v2(
        valid_email_2, 
        valid_password_2, 
        valid_first_name_2, 
        valid_last_name_2)['token']

    for user in users:
        if user['token'] == new_token_1:
            user_1_handle = user['handle']

    new_handle = user_1_handle

    with pytest.raises(InputError):
        user_profile_sethandle_v1(new_token_2, new_handle)