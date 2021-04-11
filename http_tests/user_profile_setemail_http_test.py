import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_setemail_v1
from src.error import InputError



def test_valid_user_email():
    requests.delete(config.url + 'clear/v1')

    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_email = 'newemail@valid.com'
    data_2 = {
        'token': token_1,
        'email': new_email
    }
    #print(data_3)

    resp_user_profile = requests.put(config.url + 'user/profile/setemail/v1', json=data_2)
    assert resp_user_profile.status_code == 200

def test_invalid_user_email():
    requests.delete(config.url + 'clear/v1')

    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    token_1 = resp_register_1.json().get('token')
    new_email = 'newinvalidemail.com'
    data_2 = {
        'token': token_1,
        'email': new_email
    }
    #print(data_3)

    resp_user_profile = requests.put(config.url + 'user/profile/setemail/v1', json=data_2)
    assert resp_user_profile.status_code == 400

def test_user_profile_setemail_used():
    data_1 = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }
    
    data_2 = {
        'email': 'abc@defgh.com',
        'password': 'Password01!',
        'name_first': 'steve',
        'name_last': 'Smith'
    }

    resp_register_1 = requests.post(config.url + 'auth/register/v2', json=data_1)
    resp_register_2 = requests.post(config.url + 'auth/register/v2', json=data_2)
    token_1 = resp_register_1.json().get('token')
    token_2 = resp_register_2.json().get('token')
    new_email = 'abc@defgh.com'
    
    data_3 = {
        'token': token_1,
        'email': new_email
    }

    resp_user_setemail = requests.put(config.url + 'user/profile/setemail/v1', json=data_3)
    assert resp_user_setemail.status_code == 400
