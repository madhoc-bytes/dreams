# HTTP Test File for message/send/v1

# Imports
import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError


def test_valid_message_pin():
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

    # Testing sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)
    message_id = r.json().get('message_id')

    pin_data = {'token': token, 'message_id': message_id}
    r = requests.put(config.url + 'message/pin/v1', json=pin_data)

    assert r.status_code == 200

def test_long_message_send():
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

    # Testing sending message
    message = 'a' * 1001
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)

    assert r.status_code == 400

def test_message_send_not_authorised_user():
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


    # Testing sending message
    message = 'a'
    message_data = {'token': token, 'channel_id': ch_id, 'message': message}
    r = requests.post(config.url + 'message/send/v1', json=message_data)

    assert r.status_code == 403