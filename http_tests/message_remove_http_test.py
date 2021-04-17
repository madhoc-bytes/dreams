# HTTP Test File for message/share/v1 

# Imports
import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError


def test_message_remove_from_channel_invalid_message():
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

    # Sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    # Test removing the same message
    remove_data = {'token': token, 'message_id': message_id}
    r1 = requests.delete(config.url + 'message/remove/v1', json=remove_data)
    r2 = requests.delete(config.url + 'message/remove/v1', json=remove_data)
    

    assert r2.status_code == 400

def test_message_remove_from_channel_not_sent_by_same_user():
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
    token_2 = r.json().get('token')

    
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

    # Sending message from user 1
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    # Test removing the message from user 2
    remove_data = {'token': token_2, 'message_id': message_id}
    r = requests.delete(config.url + 'message/remove/v1', json=remove_data)

    assert r.status_code == 403

def test_message_remove_from_channe():
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

    # Sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    # Test removing the message
    remove_data = {'token': token, 'message_id': message_id}
    r = requests.delete(config.url + 'message/remove/v1', json=remove_data)

    assert r.status_code == 200

def test_message_remove_from_dm():
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

    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)

    u_id2 = r.json().get('auth_user_id')

    # Create DM 1
    create_data = {
        'token': token,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id_1 = r.json().get('dm_id')

    # Create DM 2
    create_data = {
        'token': token,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)



    # Sending a message to dm 1
    message = 'a'
    message_data = {'token': token, 'dm_id': dm_id_1, 'message': message}
    r = requests.post(config.url + '/message/senddm/v2', json=message_data)
    message_id = r.json().get('message_id')

    # Test removing the message
    remove_data = {'token': token, 'message_id': message_id}
    r = requests.delete(config.url + 'message/remove/v1', json=remove_data)

    assert r.status_code == 200