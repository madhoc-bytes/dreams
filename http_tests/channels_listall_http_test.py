# HTTP Test File for channels/listall/v2 

# Imports
import pytest
import requests
import json
from src import config
import flask 

# Test for one user with no channels created
def test_no_channels_listall():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register user
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token
    payload = r.json()
    token = payload['token']
    
    # Get list of channels for that user
    resp = requests.get(config.url + 'channels/listall/v2', params=token, methods='GET')

    # Assertions
    assert(resp.status_code = 200 and json.loads(resp.text) == {})


# Test for one channel
def test_one_channel_listall():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register one user
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')

    # Get the token
    payload = r.json()
    token = payload['token']
    
    # Create a channel with user in it
    create_data = {token, 'My Unique Channel', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id = payload['channel_id']
    
    # Make the user join channel
    join_data = {token, channel_id}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Get result
    resp = requests.get(config.url + 'channels/listall/v2', params=token, methods='GET')
    
    # Assertions
    assert(resp.status_code = 200 and json.loads(resp.text) == [{'name': 'My Unique Channel',
                                                                'all_members': [
                                                                    {
                                                                        'u_id': 0,
                                                                        'name_first': 'Jack',
                                                                        'name_last': 'Germani',
                                                                    }
                                                                ]
                                                                
                                                                }])



# Test for two channels and one user
def test_two_channels_listall():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register a user
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')

    # Get the token
    payload = r.json()
    token = payload['token']
    
    # Create first channel with user in it
    create_data = {token, 'Channel 1', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_1 = payload['channel_id']

    # Create second channel with user in it
    create_data = {token, 'Channel 2', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_2 = payload['channel_id']
    
    # Make the user join both channels
    join_data = {token, channel_id_1}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')
    join_data = {token, channel_id_2}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Get result
    resp = requests.get(config.url + 'channels/listall/v2', params=token, methods='GET')
    
    # Assertions
    assert(resp.status_code = 200 and json.loads(resp.text) == [{'name': 'Channel 1',
                                                                'all_members': [
                                                                    {
                                                                        'u_id': 0,
                                                                        'name_first': 'Jack',
                                                                        'name_last': 'Germani',
                                                                    }
                                                                ]
                                                                
                                                                }, {
                                                                'name': 'Channel 2',
                                                                
                                                                'all_members': [
                                                                    {
                                                                        'u_id': 0,
                                                                        'name_first': 'Jack',
                                                                        'name_last': 'Germani',
                                                                    }
                                                                ] 
                                                                }])


# Test for 3 channels in which user has only access to 1
def test_two_users_channels():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register user 1 and get token
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    payload = r.json()
    token_user_1 = payload['token']
    
    # Register user 2 and get token
    register_data = {'email': 'elonmusk@yahoo.com', 'password': 'bitcoin777', 'name_first': 'Elon', 'name_last': 'Musk'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    payload = r.json()
    token_user_2 = payload['token']

    # Create first channel with user 1 in it
    create_data = {token_user_1, 'Jack Channel', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_1 = payload['channel_id']

    # Create second channel with user 2 in it
    create_data = {token_user_2, 'Elon Channel 1', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_2 = payload['channel_id']

    # Create third channel with user 2 in it
    create_data = {token_user_2, 'Elon Channel 2', True}
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    payload = r.json()
    channel_id_3 = payload['channel_id']
    
    # Make user 1 join channel 1
    join_data = {token_user_1, channel_id_1}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # Make user 2 join channel 2
    join_data = {token_user_2, channel_id_2}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')
    
    # Make user 2 join channel 3
    join_data = {token_user_2, channel_id_3}
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    # List all channels for user 1
    resp = requests.get(config.url + 'channels/listall/v2', params=token_user_1, methods='GET')

    # Assertions
    assert(assert resp.status_code = 200 and channels_listall_v1(user1_id) == [{'name': 'Jack Channel',
                                                                                'all_members': [
                                                                                    {
                                                                                        'u_id': 0,
                                                                                        'name_first': 'Jack',
                                                                                        'name_last': 'Germani',
                                                                                    }
                                                                                ]
                                                                                
                                                                                }, {
                                                                                'name': 'Elon Channel 1',
                                                                                'all_members': [
                                                                                    {
                                                                                        'u_id': 1,
                                                                                        'name_first': 'Elon',
                                                                                        'name_last': 'Musk',
                                                                                    }
                                                                                ] 
                                                                                }, {
                                                                                    'name': 'Elon Channel 2',
                                                                                'all_members': [
                                                                                    {
                                                                                        'u_id': 1,
                                                                                        'name_first': 'Elon',
                                                                                        'name_last': 'Musk',
                                                                                    }
                                                                                ]
                                                                                }])