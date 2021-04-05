import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_logout_v2


def test_logout_valid():
    data_register = json.dumps({
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        })
    data_login = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!'
    })

    resp_register = requests.post(config.url + 'auth/register/v2', data=data_register)
    #resp_login = requests.post(config.url + 'auth/login/v2', data=data_login)
    user_dict = json.loads(resp_register.text)
    token1 = user_dict['token']
    

    resp_logout = requests.post(config.url + 'auth/logout/v2', data=token1)
    assert resp_logout.status_code == 200
    #assert json.loads(resp_logout.text) == {'is_success': True}