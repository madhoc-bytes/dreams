import pytest
import requests
import json
from src import config

def test_valid():
    requests.delete(config.url + 'clear/v2')

    # register 2 users
    reg_data1 = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    reg_data2 = json.dumps({
        'email': 'test1@gmail.com',
        'password': 'testpw1234',
        'name_first': 'test_fname1',
        'name_last': 'test_lname1'
    })

    # acquire token of inviter and id of invitee
    r = requests.post(config.url + 'auth/register/v2', data=reg_data1)
    token1 = r.json().get('token')

    r = requests.post(config.url + 'auth/register/v2', data=reg_data2)
    user2_id = r.json().get('auth_user_id')

    # create a channel
    ch_data = json.dumps({
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # add user1 to the channel
    join_data = json.dumps({
        'token': token1,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data)

    # let user1 invite user2
    invite_data = json.dumps({
        'token': token1,
        'channel_id': ch_id,
        'u_id': user2_id
    })

    # testing channel invite v2
    r = requests.post(config.url + 'channel/invite/v2', data=invite_data)
    assert r.status_code == 200

def test_invite_channel_invalid():
    requests.delete(config.url + 'clear/v2')

    # register 2 users
    reg_data1 = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    reg_data2 = json.dumps({
        'email': 'test1@gmail.com',
        'password': 'testpw1234',
        'name_first': 'test_fname1',
        'name_last': 'test_lname1'
    })

    # acquire token of inviter and id of invitee
    r = requests.post(config.url + 'auth/register/v2', data=reg_data1)
    token1 = r.json().get('token')

    r = requests.post(config.url + 'auth/register/v2', data=reg_data2)
    user2_id = r.json().get('auth_user_id')

    # try to invite 1 to a non-existent channel and expect inputerror
    invalid_id = 10
    invite_data = json.dumps({
        'token': token1,
        'channel_id': invalid_id,
        'u_id': user2_id
    })
    r = requests.post(config.url + 'channel/invite/v2', data=invite_data)
    assert r.status_code == 400

def test_invite_user_invalid():
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

    # try to add non-existent user to channel and expect inputerror
    invalid_id = 10
    invite_data = json.dumps({
        'token': token,
        'channel_id': ch_id,
        'u_id': invalid_id
    })
    r = requests.post(config.url + 'channel/invite/v2', data=invite_data)
    assert r.status_code == 400

def test_invite_inviter_not_in_channel():
    requests.delete(config.url + 'clear/v2')

    # register 2 users
    reg_data1 = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    reg_data2 = json.dumps({
        'email': 'test1@gmail.com',
        'password': 'testpw1234',
        'name_first': 'test_fname1',
        'name_last': 'test_lname1'
    })

    # acquire token of inviter and id of invitee
    r = requests.post(config.url + 'auth/register/v2', data=reg_data1)
    token1 = r.json().get('token')

    r = requests.post(config.url + 'auth/register/v2', data=reg_data2)
    user2_id = r.json().get('auth_user_id')

    # create a channel
    ch_data = json.dumps({
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # try to invite users to channel when inviter is not in channel and 
    # expect access error
    invite_data = json.dumps({
        'token': token1,
        'channel_id': ch_id,
        'u_id': user2_id
    })

    # testing channel invite v2
    r = requests.post(config.url + 'channel/invite/v2', data=invite_data)
    assert r.status_code == 403