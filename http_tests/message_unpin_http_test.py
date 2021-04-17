# HTTP Test File for message/send/v1


# Imports
import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError



def test_valid_message_pin_channel():
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

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)

    # sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    pin_data = {'token': token, 'message_id': message_id}
    requests.post(config.url + 'message/pin/v1', json=pin_data)
    unpin_data = {'token': token, 'message_id': message_id}
    r = requests.post(config.url + 'message/unpin/v1', json=unpin_data)

    assert r.status_code == 200

def test_unpin_message_unpinned():

    requests.delete(config.url + '/clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + '/auth/register/v2', json=reg_data)
    token = r.json()['token']

    
    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + '/channels/create/v2', json=ch_data)
    ch_id = r.json()['channel_id']

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    requests.post(config.url + '/channel/join/v2', json=join_data)


    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + '/message/send/v1', json=message_data)
    message_id = r.json()['message_id']

    pin_data = {'token': token, 'message_id': message_id}
    requests.post(config.url + '/message/pin/v1', json=pin_data)
    unpin_data = {'token': token, 'message_id': message_id}
    requests.post(config.url + '/message/unpin/v1', json=unpin_data)
    r2 = requests.post(config.url + '/message/unpin/v1', json=unpin_data)
    
    assert r2.status_code == 400

def test_pin_message_not_authorised_user():
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

    # register a user
    reg_data = {
        'email': 'test123@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token2 = r.json().get('token')

    
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

    # Testing sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    pin_data = {'token': token, 'message_id': message_id}
    requests.post(config.url + 'message/pin/v1', json=pin_data)
    unpin_data = {'token': token2, 'message_id': message_id}
    r1 = requests.post(config.url + 'message/unpin/v1', json=unpin_data)

    assert r1.status_code == 403

def test_pin_message_dm():
    requests.delete(config.url + 'clear/v1')

    #owner of dm/caller of dm_create
    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    auth_id = r.json().get('auth_user_id')


    # Create DM 1
    create_data = {
        'token': token,
        'u_ids': [auth_id]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id_1 = r.json().get('dm_id')


    # Sending a message to dm 
    message = 'a'
    message_data = {'token': token, 'dm_id': dm_id_1, 'message': message}
    r = requests.post(config.url + '/message/senddm/v2', json=message_data)
    message_id = r.json().get('message_id')

    # Test pinning the message
    pin_data = {'token': token, 'message_id': message_id}
    requests.post(config.url + 'message/pin/v1', json=pin_data)
    unpin_data = {'token': token, 'message_id': message_id}
    r1 = requests.post(config.url + 'message/unpin/v1', json=unpin_data)

    assert r1.status_code == 200