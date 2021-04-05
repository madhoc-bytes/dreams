import pytest 
from src.user import user_profile_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_sethandle_v1
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.data import users
from src.other import clear_v1

def test_user_profile_valid():
    clear_v1()

    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    new_user_id_1 = auth_register_v2(
            valid_email_1, 
            valid_password_1, 
            valid_first_name_1, 
            valid_last_name_1)['auth_user_id']
    
    
    valid_email_2, valid_password_2 = 'abc@defg.com', 'helloWorld123!'
    valid_first_name_2, valid_last_name_2 = 'mitchel', 'johnson'
    new_user_id_2 = auth_register_v2(
            valid_email_2, 
            valid_password_2, 
            valid_first_name_2, 
            valid_last_name_2)['auth_user_id']
    
    for user in users:
        if user['u_id'] == new_user_id_2:
            handle_user_2 = user['handle']

    user_profile_info = {}
    user_profile_info = user_profile_v1(new_user_id_1, new_user_id_2)

    assert user_profile_info == {'user': {
            'u_id': new_user_id_2,
            'email': valid_email_2,
            'name_first': valid_first_name_2,
            'name_last': valid_last_name_2,
            'handle_str': handle_user_2,
        },
        }

def test_invalid_user():
    clear_v1()

    valid_email_1, valid_password_1 = 'abc@def.com', 'helloWorld123!'
    valid_first_name_1, valid_last_name_1 = 'steve', 'smith'
    
    new_user_id_1 = auth_register_v2(
        valid_email_1, 
        valid_password_1, 
        valid_first_name_1, 
        valid_last_name_1)['auth_user_id']


    valid_email_2, valid_password_2 = 'abc@defg.com', 'helloWorld123!'
    valid_first_name_2, valid_last_name_2 = 'mitchel', 'johnson'
    
    auth_register_v2(
        valid_email_2, 
        valid_password_2, 
        valid_first_name_2, 
        valid_last_name_2)

    invalid_user_id = 5

    with pytest.raises(InputError):
        user_profile_v1(new_user_id_1, invalid_user_id)