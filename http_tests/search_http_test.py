import pytest
import requests
import json
from src import config

def test_valid():
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

    search_data = {
        'token': token,
        'query_str': 'test'
    }

    r = requests.get(config.url + 'search/v2', params=search_data)
    assert r.status_code == 200

    # create a channel
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
    requests.post(config.url + 'channel/join/v2', json=join_data)

    #send messages
    msg_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'test1'   
    }
    requests.post(config.url + 'message/send/v1', json=msg_data)

    msg_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'test2'   
    }
    requests.post(config.url + 'message/send/v1', json=msg_data)
    

    r = requests.get(config.url + 'search/v2', params=search_data)
    assert r.status_code == 200

def test_long_querystr():
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

    long_str = 'a' * 1001
    search_data = {
        'token': token,
        'query_str': long_str
    }

    r = requests.get(config.url + 'search/v2', params=search_data)
    assert r.status_code == 400





