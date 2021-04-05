'''import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_v1
from src.error import InputError

def test_user_profile_setname_valid():

    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    #user_info = 

    data_2 = json.dumps({
        'token': token_1,
        'new_name_first': 'mitch',
        'new_name_last': 'johnson'
    })

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_profile.status_code == 200

def test_first_name_too_short():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J',
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_profile.status_code == 400

def test_first_name_too_long():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J'*52,
        'name_last': 'Smith'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_profile.status_code == 400

def test_last_name_too_short():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_profile.status_code == 400

def test_last_name_too_long():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'*52
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_profile.status_code == 400'''