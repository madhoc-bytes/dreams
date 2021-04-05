import pytest
import requests
import json
from src import config

def test_basic():
    requests.delete(config.url + 'clear/v1')

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

    # acquire id and token of inviter and invitee
    r = requests.post(config.url + 'auth/register/v2', json=reg_data1)
    token1 = r.json().get('token')
    user1_id = r.json().get('auth_user_id')    

    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    user2_id = r.json().get('auth_user_id')

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

    # make users owners
    addowner_data = {
        'token': token1,
        'channel_id': ch_id,
        'u_id': user1_id
    }
    requests.post(config.url + 'channel/addowner/v1', json=addowner_data)

    addowner_data = {
        'token': token1,
        'channel_id': ch_id,
        'u_id': user2_id
    }
    requests.post(config.url + 'channel/addowner/v1', json=addowner_data)

    # remove user2 ownership
    removeowner_data = {
        'token': token1,
        'channel_id': ch_id,
        'u_id': user2_id
    }
    r = requests.post(config.url + 'channel/removeowner/v1', json=removeowner_data)
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

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    u_id = r.json().get('auth_user_id')

    # try to remove owner from a non-existent channel and expect failure
    invalid_id = 10
    removeowner_data = {
        'token': token,
        'channel_id': invalid_id,
        'u_id': u_id
    }

    # testing channel removeowner v2
    r = requests.post(config.url + 'channel/removeowner/v1', json=removeowner_data)
    assert r.status_code == 400

def test_not_an_owner():
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

    # add user to the channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }    
    requests.post(config.url + 'channel/join/v2', json=join_data)    
    
    # try to remove user ownership, when user is not owner and expect input error
    removeowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    }
    r = requests.post(config.url + 'channel/removeowner/v1', json=removeowner_data)
    assert r.status_code == 400

def test_only_owner():
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

    # make user an owner
    addowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    }
    requests.post(config.url + 'channel/addowner/v1', json=addowner_data)  
    
    # try to remove user ownership when user is the only owner and expect input error
    removeowner_data = {
        'token': token,
        'channel_id': ch_id,
        'u_id': u_id
    }
    r = requests.post(config.url + 'channel/removeowner/v1', json=removeowner_data)
    assert r.status_code == 400

def test_no_privileges():
    requests.delete(config.url + 'clear/v1')

    # register 3 users
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

    reg_data3 = {
        'email': 'test2@gmail.com',
        'password': 'testpw12345',
        'name_first': 'test_fname2',
        'name_last': 'test_lname2'
    }

    # acquire id and token of users
    r = requests.post(config.url + 'auth/register/v2', json=reg_data1)
    token1 = r.json().get('token')
    user1_id = r.json().get('auth_user_id')    

    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    user2_id = r.json().get('auth_user_id')

    r = requests.post(config.url + 'auth/register/v2', json=reg_data3)
    token3 = r.json().get('token')

    # create a channel
    ch_data = {
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # make user1 and user2 owners
    addowner_data = {
        'token': token1,
        'channel_id': ch_id,
        'u_id': user1_id
    }    
    requests.post(config.url + 'channel/addowner/v1', json=addowner_data)

    addowner_data = {
        'token': token1,
        'channel_id': ch_id,
        'u_id': user2_id
    }    
    requests.post(config.url + 'channel/addowner/v1', json=addowner_data)

    # add user3 to channel as a regular member
    join_data = {
        'token': token3,
        'channel_id': ch_id
    }    
    requests.post(config.url + 'channel/join/v2', json=join_data)

    # try to let non-owner (user3) remove user1's ownership and expect accesserror
    removeowner_data = {
        'token': token3,
        'channel_id': ch_id,
        'u_id': user1_id
    }
    r = requests.post(config.url + 'channel/removeowner/v1', json=removeowner_data)
    assert r.status_code == 403