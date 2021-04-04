# HTTP Test File for message/share/v1 

# Imports
import pytest
import requests
import json
from src import config
import flask
from error import InputError, AccessError


# AccessError test
def test_share_message_to_channel_user_not_joined():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register user
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token
    payload = r.json()
    token = payload['token']

    # Create message
    message = 'a' * 1001

    # Create a channel 
    create_data = {'token': token, 'name': 'My Channel', 'is_public': True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']

    # Create a second channel
    create_data = {'token': token, 'name': 'My Channel', 'is_public': True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_2 = payload['channel_id']

    # Make the user join channel 1
    join_data = {'token': token, 'channel_id': channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Send message to channel 1
    message_data = {'token': token, 'channel_id': channel_id, 'message': message}
    r = requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')
    payload = r.json()
    message_id = payload['message_id']

    # Share message to channel 2
    dm_id = -1
    message = 'Test'
    share_id = {'token': token, 'message_id': message_id, 'message': message, 'channel_id': channel_id, 'dm_id': dm_id}

    # Assertions
    assert resp.status_code == 403


# Test normal message with authorised user in channel
def test_share_message_to_channel():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register user
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token
    payload = r.json()
    token = payload['token']

    # Create message
    message = 'This project is so hard!!'

    # Create a channel 
    create_data = {'token': token, 'name': 'My Channel', 'is_public': True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']

    # Create a second channel
    create_data = {'token': token, 'name': 'My Channel', 'is_public': True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_2 = payload['channel_id']

    # Make the user join channel 1
    join_data = {'token': token, 'channel_id': channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Make the user join channel 2
    join_data = {'token': token, 'channel_id': channel_id_2}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Send message to channel 1
    message_data = {'token': token, 'channel_id': channel_id, 'message': message}
    r = requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')
    payload = r.json()
    message_id = payload['message_id']

    # Share message to channel 2
    dm_id = -1
    message = 'Test'
    share_id = {'token': token, 'message_id': message_id, 'message': message, 'channel_id': channel_id, 'dm_id': dm_id}

    # Assertions
    assert resp.status_code == 200

