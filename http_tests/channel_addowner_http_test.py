import pytest
import requests
import json
from src import config

def test_basic():
    requests.delete(config.url + 'clear/v2')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)
    token = r.json().get('token')
    u_id = r.json().get('auth_user_id')

    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # testing channel addowner v2
    addowner_data = json.dumps({
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    })    
    r = requests.post(config.url + 'channel/addowner/v2', data=addowner_data)
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

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)
    token = r.json().get('token')
    u_id = r.json().get('auth_user_id')

    # try to add owner to a non-existent channel and expect failure
    invalid_id = 10
    addowner_data = json.dumps({
        'token': token,
        'channel_id': invalid_id,
        'u_id': u_id
    })

    # testing channel addowner v2
    r = requests.post(config.url + 'channel/addowner/v2', data=addowner_data)
    assert r.status_code == 400

def test_already_owner():
    requests.delete(config.url + 'clear/v2')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)
    token = r.json().get('token')
    u_id = r.json().get('auth_user_id')

    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # make user an owner
    addowner_data = json.dumps({
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    })    
    requests.post(config.url + 'channel/addowner/v2', data=addowner_data)

    # try to make user owner again and expect input error
    r = requests.post(config.url + 'channel/addowner/v2', data=addowner_data)
    assert r.status_code == 400

def test_no_privileges():
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

    # acquire id and token of inviter and id of invitee
    r = requests.post(config.url + 'auth/register/v2', data=reg_data1)
    token1 = r.json().get('token')
    user1_id = r.json().get('auth_user_id')

    r = requests.post(config.url + 'auth/register/v2', data=reg_data2)
    token2 = r.json().get('token')

    # create a channel
    ch_data = json.dumps({
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    })

    # acquire channel id
    r = requests.post(config.url + 'channels/create', data=ch_data)
    ch_id = r.json().get('channel_id')

    # add users to the channel
    join_data = json.dumps({
        'token': token1,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data)

    join_data = json.dumps({
        'token': token2,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data)

    # try to let non-owner (user2) make user1 an owner and expect accesserror
    addowner_data = json.dumps({
        'token': token2,
        'channel_id': ch_id,
        'u_id': user1_id
    })
    r = requests.post(config.url + 'channel/addowner/v2', data=addowner_data)
    assert r.status_code == 403