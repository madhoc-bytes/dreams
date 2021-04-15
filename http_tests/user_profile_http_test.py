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



def test_valid_user_profile():
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
        'name_first': 'mitchel',
        'name_last': 'johnson'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json()['token']
    resp_register_2 = requests.post(config.url + 'auth/register/v2', json=data_2)
    u_id_2 = resp_register_2.json()['auth_user_id']
    data_3 = {
        'token': token_1,
        'u_id': u_id_2
    }
    print(data_3)

    resp_user_profile = requests.get(config.url + 'user/profile/v1', params=data_3)
    assert resp_user_profile.status_code == 200


def test_invalid_user():
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
        'name_first': 'mitchel',
        'name_last': 'johnson'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json()['token']
    requests.post(config.url + 'auth/register/v2', json=data_2)
    u_id_2 = 4
    data_3 = {
        'token': token_1,
        'u_id': u_id_2
    }

    resp_user_profile = requests.get(config.url + 'user/profile/v1', params=data_3)
    assert resp_user_profile.status_code == 400
