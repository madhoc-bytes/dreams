import pytest 
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_sethandle_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.data import users
from src.other import clear_v1

def test_user_profile_setemail_valid():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']

    new_email = 'thisisnew@email.com'

    user_profile_setemail_v1(new_token_1, new_email)

    for user in users:
        if user['token'] == new_token_1:
            user_info = user

    assert user_info['email'] == new_email

def test_invalid_email():
    clear_v1()
    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_token_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['token']

    invalid_new_email = 'thisisinvalidemail.com'

    with pytest.raises(InputError):
        user_profile_setemail_v1(new_token_1, invalid_new_email)

def test_used_email():
    clear_v1()

    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    auth_register_v2(
        valid_email_1, 
        valid_password_1, 
        valid_first_name_1, 
        valid_last_name_1)
    
    
    valid_email_2, valid_password_2 = 'abc@defg.com', 'helloWorld123!'
    valid_first_name_2, valid_last_name_2 = 'mitchel', 'johnson'
    new_token_2 = auth_register_v2(
        valid_email_2, 
        valid_password_2, 
        valid_first_name_2, 
        valid_last_name_2)['token']

    with pytest.raises(InputError):
        user_profile_setemail_v1(new_token_2, valid_email_1)