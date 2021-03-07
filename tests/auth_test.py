import pytest 
from src.auth import auth_register_v1
from src.error import InputError
from src.data import users


def test_auth_register_valid():
    #clear_v1()
    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    new_user_id = auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']

    valid_email1, valid_password1 = 'ab1c@def.com', 'hell1oWorld123!'
    valid_first_name1, valid_last_name1 = 'joh1n', 'smit1h'
    new_user_id1 = auth_register_v1(
            valid_email, 
            valid_password, 
            valid_first_name, 
            valid_last_name)['auth_user_id']
            


    assert users[new_user_id1] == {
            'email': valid_email,
            'password': valid_password,
            'name_first': valid_first_name,
            'name_last':  valid_last_name,
            'handle': valid_first_name + valid_last_name,
            'u_id': 0,
    }

def test_auth_register_invalid_email():
    #clear_v1()
    valid_password = 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    
    invalid_email = 'abc.com'
    
    with pytest.raises(InputError):
        auth_register_v1(invalid_email, valid_password, valid_first_name, valid_last_name)

def test_auth_register_short_password():
    #clear_v1()
    # if password string less than 6 characters raise error
    valid_email, valid_first_name, valid_last_name = 'abc@def.com', 'john', 'smith'
    short_password = 'hello1'

    #user = auth.auth_register_v1(valid_email, short_password, valid_first_name, valid_last_name) 

    with pytest.raises(InputError):
        auth_register_v1(valid_email, short_password, valid_first_name, valid_last_name)

def test_auth_register_short_first_name():
    #clear_v1()
    # if first_name string is less than 1 character, raise error
    valid_email, valid_password, valid_last_name = 'abc@def.com', 'helloWorld123!', 'lo'
    short_first_name = 'a'

    #user = auth.auth_register_v1(valid_email, valid_password, short_first_name, valid_last_name) 

    with pytest.raises(InputError):
        auth_register_v1(valid_email, valid_password,short_first_name, valid_last_name)

def test_auth_register_long_first_name():
    #clear_v1()
    # if the first_name is longer than 50 characters, raise error
    valid_email, valid_password, valid_last_name = 'email@email.com', 'helloWorld123!', 'lo'
    long_first_name = 'a * 52'
    
    #user = auth.auth_register_v1(valid_email, valid_password, long_first_name, valid_last_name) 

    with pytest.raises(InputError):
        auth_register_v1(valid_email, valid_password,long_first_name, valid_last_name)

def test_auth_register_short_last_name():
    #clear_v1()
    # if last_name string is less than 1 character, raise error
    valid_email, valid_password, valid_first_name = 'abc@def.com', 'helloWorld123!', 'jo'
    short_last_name = 'b'

    #user = auth.auth_register_v1(valid_email, valid_password, valid_first_name, long_last_name) 

    with pytest.raises(InputError):
        auth_register_v1(valid_email, valid_password,valid_first_name, short_last_name)

def test_auth_register_long_last_name():
    #clear_v1()
    # if last_name is longer than 50 characters, raise error
    valid_email, valid_password, valid_first_name = 'abc@def.com', 'helloWorld123!', 'jo'
    long_last_name = 'b * 52'

    #user = auth.auth_register_v1(valid_email, valid_password, valid_first_name, long_last_name) 
    
    with pytest.raises(InputError):
        auth_register_v1(valid_email, valid_password,valid_first_name, long_last_name)


