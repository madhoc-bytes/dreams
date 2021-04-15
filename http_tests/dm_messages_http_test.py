import pytest
import requests
import json
from src import config
import flask 

def test_dm_messages_nomessage():
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

    msg_params = {
        'token': token,
        'dm_id': dm_id,
        'start': 0
    }

    r = requests.get(config.url + 'dm/messages/v1', params=msg_params)
    assert r.status_code == 200

def test_dm_messages_invalid_d_id():
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

    msg_params = {
        'token': token,
        'dm_id': 10,
        'start': 0
    }

    r = requests.get(config.url + 'dm/messages/v1', params=msg_params)

    assert r.status_code == 400

def test_dm_messages_start_too_big():
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

    msg_params = {
        'token': token,
        'dm_id': dm_id,
        'start': 2
    }

    r = requests.get(config.url + 'dm/messages/v1', params=msg_params)

    assert r.status_code == 400

def test_dm_messages_not_member():
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

    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')

    create_data = {
        'token': token,
        'u_ids': []
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    msg_params = {
        'token': token2,
        'dm_id': dm_id,
        'start': 0
    }

    r = requests.get(config.url + 'dm/messages/v1', params=msg_params)

    assert r.status_code == 403
