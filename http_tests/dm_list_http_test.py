import pytest
import requests
import json
from src import config
import flask 

def test_dm_list_basic():    
    requests.delete(config.url + 'clear/v1')

    #owner of dm/caller of dm_create
    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    list_params = {
        'token': token
    }

    r = requests.get(config.url + 'channel/list/v2', params=list_params)