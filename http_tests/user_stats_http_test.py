import pytest
import requests
import json
from src import config

def test_system():
    requests.delete(config.url + 'clear/v1')
    
    # register a user
    reg_data1 = {
        'email': 'test1@gmail.com',
        'password': 'testpw1',
        'name_first': 'test_fname1',
        'name_last': 'test_lname1'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data1)

    # acquire token of user
    token1 = r.json().get('token')

    # create a channel
    ch_data = {
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    }
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    
    # acquire channel id    
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token1,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)

    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test2@gmail.com',
        'password': 'testpw2',
        'name_first': 'test_fname2',
        'name_last': 'test_lname2'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)

    # get id of user2
    u_id2 = r.json().get('auth_user_id')

    create_data = {
        'token': token1,
        'u_ids': [u_id2]
    }
    r = requests.post(config.url + 'dm/create/v1', json=create_data)

    dm_id = r.json().get('dm_id')

    message_data = {'token': token1, 'dm_id': dm_id, 'message': 'hello'}
    r = requests.post(config.url + 'message/senddm/v1', json=message_data)

    stats_params = {
        'token': token1
    }
    r = requests.get(config.url + 'user/stats/v1', params=stats_params)

    assert r.status_code == 200
