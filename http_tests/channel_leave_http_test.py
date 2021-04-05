import pytest
import requests
import json
from src import config

def test_basic():
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
    u_id = r.json().get('auth_user_id')
    
    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # add user to channel as an owner
    addowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    }    
    r = requests.post(config.url + 'channel/addowner/v1', json=addowner_data)

    # user leave
    leave_data = {
        'token': token,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/leave/v2', json=leave_data)
    assert r.status_code == 200

def test_invalid_channel():    
    requests.delete(config.url + 'clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire tokenof user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    invalid_id = 10

    # try to leave from non-existent channel and expect input error
    invalid_id = 10
    leave_data = {
        'token': token,
        'channel_id': invalid_id
    }   
    r = requests.post(config.url + 'channel/leave/v2', json=leave_data)
    assert r.status_code == 400

def test_unauthorised_user():
    requests.delete(config.url + 'clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    
    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # try to call channel_leave when auth_user is not in the channel and expect failure
    leave_data = {
        'token': token,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/leave/v2', json=leave_data)
    assert r.status_code == 403