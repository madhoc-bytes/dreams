import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_sethandle_v1
from src.error import InputError

def test_user_profile_sethandle_valid():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_handle = 'thisisnewhandle'
    print(resp_register_1.status_code)
    print(token_1)

    data_2 = {
        'token': token_1,
        'handle_str': new_handle
    }
    print(data_2)
    resp_user_sethandle = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    print(resp_user_sethandle.status_code)
    assert resp_user_sethandle.status_code == 200

def test_user_profile_sethandle_used():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    
    data_2 = {
        'email': 'abc@defgh.com',
        'password': 'Password01!',
        'name_first': 'mitch',
        'name_last': 'john'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    resp_register_2 = requests.post(config.url + 'auth/register/v2', json=data_2)
    token_1 = resp_register_1.json().get('token')
    handle_used = resp_register_2.json().get('handle')
    

    data_3 = {
        'token': token_1,
        'handle_str': handle_used
    }

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_3)
    assert resp_user_setemail.status_code == 400

def test_new_handle_too_long():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_handle = 't'*25

    data_2 = {
        'token': token_1,
        'handle_str': new_handle
    }

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    assert resp_user_setemail.status_code == 400

def test_new_handle_too_short():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_handle = 't'

    data_2 = {
        'token': token_1,
        'handle_str': new_handle
    }

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    assert resp_user_setemail.status_code == 400
