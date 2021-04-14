import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_setname_v1
from src.error import InputError

def test_user_profile_setname_valid():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_name_first = 'mitch'
    new_name_last = 'johnson'

    data_2 = {
        'token': token_1,
        'name_first': new_name_first,
        'name_last': new_name_last
    }

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_setname.status_code == 200

def test_first_name_too_short():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_name_first = 'm'
    new_name_last = 'johnson'

    data_2 = {
        'token': token_1,
        'name_first': new_name_first,
        'name_last': new_name_last
    }

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_setname.status_code == 400

def test_first_name_too_long():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_name_first = 'm' *52
    new_name_last = 'johnson'

    data_2 = {
        'token': token_1,
        'name_first': new_name_first,
        'name_last': new_name_last
    }

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_setname.status_code == 400

def test_last_name_too_short():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_name_first = 'mitch'
    new_name_last = 'j'

    data_2 = {
        'token': token_1,
        'name_first': new_name_first,
        'name_last': new_name_last
    }

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_setname.status_code == 400

def test_last_name_too_long():
    requests.delete(config.url + 'clear/v1')
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_name_first = 'mitch'
    new_name_last = 'j' * 52


    data_2 = {
        'token': token_1,
        'name_first': new_name_first,
        'name_last': new_name_last
    }

    resp_user_setname = requests.put(config.url + 'user/profile/setname/v1', json=data_2)
    assert resp_user_setname.status_code == 400