import pytest
import requests
import json
from src import config
import flask 

def test_join_channel(): 
    requests.delete(config.url + 'clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    
    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    r = requests.post(config.url + 'channels/create/v2', json=ch_data)

    assert r.status_code == 200

def test_join_private():
    requests.delete(config.url + 'clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    
    # create a private channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': False
    }

    r = requests.post(config.url + 'channels/create/v2', json=ch_data)

    assert r.status_code == 400