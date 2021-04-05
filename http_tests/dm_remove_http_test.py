import pytest
import requests
import json
from src import config
import flask

def test_dm_remove_basic():
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

    create_data = {
        'token': token,
        'u_ids': []
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    rem_data = {
        'token': token,
        'dm_id': dm_id
    }

    r = requests.delete(config.url + 'dm/remove/v1', json=rem_data)
    assert r.status_code == 200

def test_dm_remove_invalid_dmid():
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

    rem_data = {
        'token': token,
        'dm_id': 2
    }

    r = requests.delete(config.url + 'dm/remove/v1', json=rem_data)
    assert r.status_code == 400
