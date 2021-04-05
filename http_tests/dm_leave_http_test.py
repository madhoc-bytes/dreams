import pytest
import requests
import json
from src import config
import flask

def test_dm_leave_basic():
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
    u_id = r.json().get('auth_user_id')

    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    u_id2 = r.json().get('auth_user_id')

    create_data = {
        'token': token,
        'u_ids': []
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    leave_data = {
        'token': token,
        'dm_id': dm_id
    }

    r = requests.post(config.url + 'dm/leave/v1', json=leave_data)
    assert r.status_code == 200

def test_dm_leave_invalid_dmid():
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
    u_id = r.json().get('auth_user_id')

    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    u_id2 = r.json().get('auth_user_id')

    create_data = {
        'token': token,
        'u_ids': []
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    leave_data = {
        'token': token,
        'dm_id': 2
    }

    r = requests.post(config.url + 'dm/leave/v1', json=leave_data)
    assert r.status_code == 400

def test_dm_leave_not_member():
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
    u_id = r.json().get('auth_user_id')

    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    u_id2 = r.json().get('auth_user_id')

    create_data = {
        'token': token,
        'u_ids': []
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    leave_data = {
        'token': token2,
        'dm_id': dm_id
    }

    r = requests.post(config.url + 'dm/leave/v1', json=leave_data)
    assert r.status_code == 403