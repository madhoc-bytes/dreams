import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_logout_v2


def test_logout_valid():
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

    requests.post(config.url + 'auth/register/v2', json=data_register)
    resp_login = requests.post(config.url + 'auth/login/v2', json=data_login)
    token = resp_login.json().get('token')

    data_logout = {
        'token': token
    }
    

    resp_logout = requests.post(config.url + 'auth/logout/v2', json=data_logout)
    assert resp_logout.status_code == 200
    #assert json.loads(resp_logout.text) == {'is_success': True}
