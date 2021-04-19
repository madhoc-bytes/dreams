import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError

def test_message_react_basic():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

    send_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'string',
    }

    r = requests.post(config.url + 'message/send/v1', json=send_data)

    react_data = {
        'token': token,
        'message_id': 0,
        'react_id': 1,
    }
    
    r = requests.post(config.url + 'message/react/v1', json=react_data)
    assert r.status_code == 200

def test_react_invalidmid():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    
    react_data = {
        'token': token,
        'message_id': 1,
        'react_id': 1,
    }

    r = requests.post(config.url + 'message/react/v1', json=react_data)
    assert r.status_code == 400

def test_react_invalidreactid():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

    send_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'string',
    }

    r = requests.post(config.url + 'message/send/v1', json=send_data)

    react_data = {
        'token': token,
        'message_id': 0,
        'react_id': 2,
    }
    
    r = requests.post(config.url + 'message/react/v1', json=react_data)
    assert r.status_code == 400


def test_already_reacted():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

    send_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'string',
    }

    r = requests.post(config.url + 'message/send/v1', json=send_data)

    react_data = {
        'token': token,
        'message_id': 0,
        'react_id': 1,
    }
    
    r = requests.post(config.url + 'message/react/v1', json=react_data)

    react_data1 = {
        'token': token,
        'message_id': 0,
        'react_id': 1,
    }
    
    r = requests.post(config.url + 'message/react/v1', json=react_data1)
    assert r.status_code == 400