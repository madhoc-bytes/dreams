import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_v1
from src.error import InputError

def test_user_profile_sethandle_valid():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    
    data_2 = json.dumps({
        'token': token_1,
        'new_handle': 'thisisnewhandle'
    })

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    assert resp_user_setemail.status_code == 200

def test_user_profile_sethandle_used():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    
    data_2 = json.dumps({
        'email': 'abc@defgh.com',
        'password': 'Password01!',
        'name_first': 'mitch',
        'name_last': 'john'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    resp_register_2 = requests.post(config.url + 'auth/register/v2', json=data_2)
    token_1 = resp_register_1.json().get('token')
    token_2 = resp_register_2.json().get('token')
    handle_used = resp_register_2.json().get('handle')

    data_3 = json.dumps({
        'token': token_1,
        'new_handle': handle_used
    })

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_3)
    assert resp_user_setemail.status_code == 400

def test_new_handle_too_long():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    
    data_2 = json.dumps({
        'token': token_1,
        'new_handle': 't'*25
    })

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    assert resp_user_setemail.status_code == 400

def test_new_handle_too_short():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    
    data_2 = json.dumps({
        'token': token_1,
        'new_handle': 't'
    })

    resp_user_setemail = requests.put(config.url + 'user/profile/sethandle/v1', json=data_2)
    assert resp_user_setemail.status_code == 400