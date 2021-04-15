import pytest
import requests
import json
from src import config
import flask 

def test_messages_nomessage():
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
    token = r.json()['token']

    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json()['channel_id']
    
    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

    messages_params = {
        'token': token, 
        'channel_id': ch_id, 
        'start': 0
    }
    r = requests.get(config.url + 'channel/messages/v2', params=messages_params)

    assert(r.status_code == 200)

def test_messages_invalid_ch_id():
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
    token = r.json()['token']
    messages_params = {
        'token': token, 
        'channel_id': 10, 
        'start': 0
    }

    r = requests.get(config.url + 'channel/messages/v2', params=messages_params)

    assert(r.status_code == 400)

def test_messages_start_too_big():
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
    token = r.json()['token']

    # create a channel
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json()['channel_id']
    
    # join user to channel
    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/join/v2', json=join_data)

def test_messages_not_member():
    requests.delete(config.url + 'clear/v1')

    #owner of dm/caller of dm_create
    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json()['token']
    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json()['token']


    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json()['channel_id']

    join_data = {
        'token': token,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/join/v2', json=join_data)
    #channel messages
    messages_params = {
        'token': token2, 
        'channel_id': ch_id, 
        'start': 0
    }

    r = requests.get(config.url + 'channel/messages/v2', params=messages_params)

    assert(r.status_code == 403)
