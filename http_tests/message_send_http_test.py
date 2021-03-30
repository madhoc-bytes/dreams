# HTTP Test File for message/send/v2 

# Imports
import pytest
import requests
import json
from src import config
import flask
from error import InputError, AccessError


# Message is more than 1000 characters
def test_message_too_long():
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

    # Create a channel with user in it
    create_data = {token, 'My Channel', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']
    
    # Make the user join channel
    join_data = {token, channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Send message
    message_data = {token, channel_id, message}
    requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')

    # Assertions: InputError
    assert resp.status_code == 400
    

# Authorised user did not join channel 
def test_not_authorised_user():
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
    create_data = {token, 'My Channel', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']
    
    # Send message
    message_data = {token, channel_id, message}
    requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')

    # Assertions: Access Error
    assert resp.status_code == 403



# Test normal message with authorised user in channel
def test_message():
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
    create_data = {token, 'My Channel', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']
    
    # Make the user join channel
    join_data = {token, channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Send message
    message_data = {token, channel_id, message}
    r = requests.post(config.url + 'message/send/v2', data=message_data, methods='POST')
    payload = r.json()
    message_id = payload['message_id']

    # MAKE SURE MESSAGE ID IS UNIQUE 

    # Assertions
    assert resp.status_code == 200

