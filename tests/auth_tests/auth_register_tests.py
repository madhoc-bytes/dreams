import pytest 
from src import auth
from .error import InputError


def test_auth_register_valid():

    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    user = auth.auth_register(valid_email, valid_password, valid_first_name, valid_last_name)

    assert auth.auth_register(valid_email, valid_password, valid_first_name, valid_last_name) == user['auth_user_id']

def test_auth_register_invalid_email():

    valid_email, valid_password = 'abc@def.com', 'helloWorld123!'
    valid_first_name, valid_last_name = 'john', 'smith'
    
    invalid_email = 'abc.com'
    
    user = auth.auth_register(valid_email, valid_password, valid_first_name, valid_last_name) 
    
    with pytest.raises(InputError) as e:
        auth.auth_register(invalid_email, valid_password, valid_first_name, valid_last_name)

def test_auth_register_short_password():
    # if password string less than 6 characters raise error
    valid_email, valid_first_name, valid_last_name = 'abc@def.com', 'john', 'smith'
    short_password = 'hello1'

    user = auth.auth_register(valid_email, short_password, valid_first_name, valid_last_name) 

    with pytest.raises(InputError)as e:
        auth.auth_register(valid_email, short_password, valid_first_name, valid_last_name)
    
def test_auth_register_short_first_name():
    # if first_name string is less than 1 character, raise error
    valid_email, valid_password, valid_last_name = 'abc@def.com', 'helloWorld123!', 'lo'
    short_first_name = 'a'

    user = auth.auth_register(valid_email, valid_password, short_first_name, valid_last_name) 

    with pytest.raises(InputError) as e:
        auth.auth_register(valid_email, valid_password,short_first_name, valid_last_name)

def test_auth_register_long_first_name():
    # if the first_name is longer than 5k0 characters, raise error
    valid_email, valid_password, valid_last_name = 'abc@def.com', 'helloWorld123!', 'lo'
    long_first_name = 'a * 52'
    
    user = auth.auth_register(valid_email, valid_password, long_first_name, valid_last_name) 

    with pytest.raises(InputError) as e:
        auth.auth_register(valid_email, valid_password,long_first_name, valid_last_name)

def test_auth_register_short_last_name():
    # if last_name string is less than 1 character, raise error
    valid_email, valid_password, valid_first_name = 'abc@def.com', 'helloWorld123!', 'jo'
    short_last_name = 'b'

    user = auth.auth_register(valid_email, valid_password, valid_first_name, long_last_name) 

    with pytest.raises(InputError) as e:
        auth.auth_register(valid_email, valid_password,valid_first_name, short_last_name)

def test_auth_register_long_last_name():
    # if last_name is longer than 50 characters, raise error
    valid_email, valid_password, valid_first_name = 'abc@def.com', 'helloWorld123!', 'jo'
    long_last_name = 'b * 52'

    user = auth.auth_register(valid_email, valid_password, valid_first_name, long_last_name) 
    
    with pytest.raises(InputError) as e:
        auth.auth_register(valid_email, valid_password,valid_first_name, long_last_name)

