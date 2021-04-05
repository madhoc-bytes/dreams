import pytest
import requests
import json
from src import config
import flask 

def test_dm_details_basic():    
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
    #create one user to pass in the list of users for dm create
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
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    details_params = {
        'token': token,
        'dm_id': dm_id
    }

    r = requests.get(config.url + 'dm/details/v1', json=details_params)
    assert r.status_code == 200

def test_dm_details_invalid_dmid():    
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
    #create one user to pass in the list of users for dm create
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
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)

    details_params = {
        'token': token,
        'dm_id': 3
    }

    r = requests.get(config.url + 'dm/details/v1', json=details_params)
    assert r.status_code == 400

def test_dm_details_not_member():    
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
    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    u_id2 = r.json().get('auth_user_id')

    reg_data3 = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data3)
    token3 = r.json().get('token')
    u_id3 = r.json().get('auth_user_id')

    create_data = {
        'token': token,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')
    details_params = {
        'token': token3,
        'dm_id': dm_id
    }

    r = requests.get(config.url + 'dm/details/v1', json=details_params)
    assert r.status_code == 403
