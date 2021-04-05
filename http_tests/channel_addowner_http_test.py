import pytest
import requests
import json
from src import config

def test_basic():
    requests.delete(config.url + 'clear/v2')

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
    
    print(f'uid = {u_id}')
    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # testing channel addowner v2
    addowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    }
    r = requests.post(config.url + 'channel/addowner/v2', json=addowner_data)
    assert r.status_code == 200

def test_invalid_channel():
    requests.delete(config.url + 'clear/v2')

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

    # try to add owner to a non-existent channel and expect failure
    invalid_id = 10
    addowner_data = {
        'token': token,
        'channel_id': invalid_id,
        'u_id': u_id
    }

    # testing channel addowner v2
    r = requests.post(config.url + 'channel/addowner/v2', json=addowner_data)
    assert r.status_code == 400

def test_already_owner():
    requests.delete(config.url + 'clear/v2')

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

    # make user an owner
    addowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    } 
    requests.post(config.url + 'channel/addowner/v2', json=addowner_data)

    # try to make user owner again and expect input error
    r = requests.post(config.url + 'channel/addowner/v2', json=addowner_data)
    assert r.status_code == 400

def test_no_privileges():
    requests.delete(config.url + 'clear/v2')

    # register 2 users
    reg_data1 = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    reg_data2 = {
        'email': 'test1@gmail.com',
        'password': 'testpw1234',
        'name_first': 'test_fname1',
        'name_last': 'test_lname1'
    }

    # acquire id and token of inviter and id of invitee
    r = requests.post(config.url + 'auth/register/v2', json=reg_data1)
    token1 = r.json().get('token')
    user1_id = r.json().get('auth_user_id')

    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')

    # create a channel
    ch_data = {
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # add users to the channel
    join_data = {
        'token': token1,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)

    join_data = {
        'token': token2,
        'channel_id': ch_id
    }    
    requests.post(config.url + 'channel/join/v2', json=join_data)

    # try to let non-owner (user2) make user1 an owner and expect accesserror
    addowner_data = {
        'token': token2,
        'channel_id': ch_id,
        'u_id': user1_id
    }
    r = requests.post(config.url + 'channel/addowner/v2', json=addowner_data)
    assert r.status_code == 403
