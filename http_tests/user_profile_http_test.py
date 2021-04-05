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



def test_valid_user_profile():
    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    
    data_2 = json.dumps({
        'email': 'abc@defgh.com',
        'password': 'Password01!',
        'name_first': 'mitchel',
        'name_last': 'johnson'
    })

    

    resp_register_1 = requests.post(config.url + 'auth/register/v2', data=data_1)
    token_1 = resp_register_1.json().get('token')
    resp_register_2 = requests.post(config.url + 'auth/register/v2', data=data_2)
    u_id_2 = resp_register_2.json().get('u_id')
    
    data_3 = json.dumps({
        'token': token_1,
        'u_id': u_id_2
    })

    resp_user_profile = requests.post(config.url + 'user/profile/v1', data=data_3)
    assert resp_user_profile.status_code == 200


def test_invalid_user():

    data_1 = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })
    
    data_2 = json.dumps({
        'email': 'abc@defgh.com',
        'password': 'Password01!',
        'name_first': 'mitchel',
        'name_last': 'johnson'
    })

    resp_register_1 = requests.post(config.url + 'auth/register/v2', data=data_1)
    token_1 = resp_register_1.json().get('token')
    resp_register_2 = requests.post(config.url + 'auth/register/v2', data=data_2)
    u_id_2 = 4

    data_3 = json.dumps({
        'token': token_1,
        'u_id': u_id_2
    })

    resp_user_profile = requests.post(config.url + 'user/profile/v1', data=data_3)
    assert resp_user_profile.status_code == 400
'''