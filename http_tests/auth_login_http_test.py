import pytest
import requests
import json
from src import config


def test_valid_login():
    
    requests.delete(config.url + 'clear/v1')


    data_register = {
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        }
    data_login = {
        'email': 'abc@def.com',
        'password': 'Password01!'
    }
    resp_register = requests.post(config.url + 'auth/register/v2', json=data_register)
    resp_login = requests.post(config.url + 'auth/login/v2', json=data_login)
    assert resp_login.status_code == 200
    #assert resp_login['token'] == str(jwt.encode({resp_login['u_id']}, da.SECRET, algorithm='HS256'))

def test_invalid_email_login():
    requests.delete(config.url + 'clear/v1')

    data_register = {
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        }
    data_login = {
        'email': 'thisisinvalid',
        'password': 'Password01!'
    }
    resp_register = requests.post(config.url + 'auth/register/v2', json=data_register)
    resp_login = requests.post(config.url + 'auth/login/v2', json=data_login)
    assert resp_login.status_code == 400

def test_unused_email_login():
    requests.delete(config.url + 'clear/v1')

    data_register = {
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        }
    data_login = {
        'email': 'def@ghi.com',
        'password': 'Password01!'
    }
    resp_register = requests.post(config.url + 'auth/register/v2', json=data_register)
    resp_login = requests.post(config.url + 'auth/login/v2', json=data_login)
    assert resp_login.status_code == 400

def test_incorrect_password_login():
    requests.delete(config.url + 'clear/v1')

    data_register = {
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        }
    data_login = {
        'email': 'def@ghi.com',
        'password': 'Password1122@'
    }
    resp_register = requests.post(config.url + 'auth/register/v2', json=data_register)
    resp_login = requests.post(config.url + 'auth/login/v2', json=data_login)
    assert resp_login.status_code == 400