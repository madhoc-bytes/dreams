# HTTP Test File for message/edit/v2 

# Imports
import pytest
import requests
import json
from src import config
import flask
from error import InputError, AccessError

# Test normal message edit with authorised user in channel
def test_message_edit():
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

    # Create a channel with user in it
    create_data = {'token': token, 'name': 'My Channel', 'is_public': True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']
    
    # Make the user join channel
    join_data = {'token': token, 'channel_id': channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Send message
    message_data = {'token': token, 'channel_id': channel_id, 'message': message}
    r = requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')
    payload = r.json()
    message_id = payload['message_id']

    # MAKE SURE MESSAGE ID IS UNIQUE 
    message_edit_data = {'token': token, 'message_id': message_id, 'message': 'Very^ Hard'}
    requests.put(config.url + 'message/send/v2', data=message_edit_data, methods='PUT')

    # Assertions
    assert resp.status_code == 200