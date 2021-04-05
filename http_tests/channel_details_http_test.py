import pytest
import requests
import json
from src import config

def test_valid():
    requests.delete(config.url + 'clear/v2')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    # acquire token
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)
    token = r.json().get('token')

    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # add inviter to channel
    join_data = json.dumps({
        'token': token,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data)

    details_params = {
        'token': token,
        'channel_id': ch_id
    }
    # testing channel details v2
    r = requests.get(config.url + 'channel/details/v2', params=details_params)
    assert r.status_code == 200

def test_invalid_channel():
    requests.delete(config.url + 'clear/v2')
    
    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })
    
    # acquire token
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)      
    token = r.json().get('token')

    # try to recall details of a non-existent channel and expect input
    # error
    invalid_id = 10
    details_params = {
        'token': token,
        'channel_id': invalid_id
    }
    r = requests.get(config.url + 'channel/details/v2', params=details_params)
    assert r.status_code == 400

def test_unauthorised_user():
    requests.delete(config.url + 'clear/v2')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    # acquire token
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)
    token = r.json().get('token')

    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })
        
    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')
    
    # testing channel details v2
    # join_data will provide the right input for channel details as well
    details_params = {
        'token': token,
        'channel_id': ch_id
    }
    
    # try to call channel_details when auth_user is not in the channel 
    # and expect access error
    r = requests.get(config.url + 'channel/details/v2', params=details_params)
    assert r.status_code == 403