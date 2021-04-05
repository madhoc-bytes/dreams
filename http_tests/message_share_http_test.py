# HTTP Test File for message/share/v1 

# Imports
import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError

def test_not_authorised_to_channel_message_share():
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
    
    # create a channel 1
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }
    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # create a channel 2 
    ch_data = {
        'token': token,
        'name': 'test_ch_2',
        'is_public': True
    }

    # acquire channel id 2
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id_2 = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)


    # Sending a message to channel 1
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    # Testing sharing the message to channel 2
    message_one = 'Sharing!'
    dm_id = -1
    share_message_data = {'token': token, 'og_message_id': message_id, 'message': message_one, 'channel_id': ch_id_2, 'dm_id': dm_id}
    r = requests.post(config.url + 'message/share/v1', json=share_message_data)

    assert r.status_code == 403

def test_valid_message_share_to_channel():
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
    
    # create a channel 1
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }
    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # create a channel 2 
    ch_data = {
        'token': token,
        'name': 'test_ch_2',
        'is_public': True
    }

    # acquire channel id 2
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id_2 = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)

    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id_2
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)

    # Sending a message to channel 1
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    # Testing sharing the message to channel 2
    message_one = 'Sharing!'
    dm_id = -1
    share_message_data = {'token': token, 'og_message_id': message_id, 'message': message_one, 'channel_id': ch_id_2, 'dm_id': dm_id}
    r = requests.post(config.url + 'message/share/v1', json=share_message_data)

    assert r.status_code == 200

def test_message_share_to_dm():
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
    u_id = r.json().get('auth_user_id')
    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
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
    dm_id_2 = r.json().get('dm_id')


    # Sending a message to dm 1
    message = 'a'
    message_data = {'token': token, 'dm_id': dm_id_1, 'message': message}
    r = requests.post(config.url + '/message/senddm/v2', json=message_data)
    message_id = r.json().get('message_id')

    # Testing sharing the message to channel 2
    message_one = 'Sharing!'
    channel_id = -1
    share_message_data = {'token': token, 'og_message_id': message_id, 'message': message_one, 'channel_id': channel_id, 'dm_id': dm_id_2}
    r = requests.post(config.url + 'message/share/v1', json=share_message_data)

    assert r.status_code == 200

def test_message_share_to_dm_user_not_in_dm():
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
    u_id = r.json().get('auth_user_id')

    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')
    u_id2 = r.json().get('auth_user_id')

    # Create DM 1
    create_data = {
        'token': token2,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id_1 = r.json().get('dm_id')

    # Create DM 2
    create_data = {
        'token': token2,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id_2 = r.json().get('dm_id')


    # Sending a message to dm 1
    message = 'a'
    message_data = {'token': token, 'dm_id': dm_id_1, 'message': message}
    r = requests.post(config.url + '/message/senddm/v2', json=message_data)
    message_id = r.json().get('message_id')

    # Testing sharing the message to channel 2
    message_one = 'Sharing!'
    channel_id = -1
    share_message_data = {'token': token, 'og_message_id': message_id, 'message': message_one, 'channel_id': channel_id, 'dm_id': dm_id_2}
    r = requests.post(config.url + 'message/share/v1', json=share_message_data)

    assert r.status_code == 403