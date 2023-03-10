# HTTP Test File for channels/list/v2 

# Imports
import pytest
import requests
import json
from src import config
import flask 

def test_no_channels_list():
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

    
    # create a channel 1
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }
    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)

    # Testing listing the channels for user
    channels_list_data = {'token': token} 
    r = requests.get(config.url + 'channels/list/v2', params=channels_list_data)

    assert json.loads(r.text) == {'channels': []} and r.status_code == 200


def test_two_channels_one_user_list():
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

    
    # create a channel 1
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id_1 = r.json()['channel_id']

    # create a channel 2
    ch_data = {
        'token': token,
        'name': 'test_ch_2',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)


    # Make user 1 join channel 1
    join_data = {
        'token': token,
        'channel_id': ch_id_1
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)


    # Testing listing the channels for user
    channels_list_data = {'token': token} 
    r = requests.get(config.url + 'channels/list/v2', params=channels_list_data)

    assert json.loads(r.text) == {'channels': [{'all_members': [{'name_first': 'test_fname', 'name_last': 'test_lname', 'u_id': 0}], 'name': 'test_ch'}]} and r.status_code == 200

def test_two_users_two_channels_list():
    requests.delete(config.url + 'clear/v1')

    # register a user 1
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json()['token']


    # register a user 2
    reg_data = {
        'email': 'test123@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token_2 = r.json()['token']
    
    # create a channel 1
    ch_data = {
        'token': token,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id_1 = r.json()['channel_id']

    # create a channel 2
    ch_data = {
        'token': token,
        'name': 'test_ch_2',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id_2 = r.json()['channel_id']

    # Make user 1 join channel 1
    join_data = {
        'token': token,
        'channel_id': ch_id_1
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)


    # Make user 2 join channel 2
    join_data = {
        'token': token_2,
        'channel_id': ch_id_2
    }   
    requests.post(config.url + 'channel/join/v2', json=join_data)


    # Testing listing the channels for user
    channels_list_data = {'token': token_2} 
    r = requests.get(config.url + 'channels/list/v2', params=channels_list_data)

    assert json.loads(r.text) == {'channels': [{'all_members': [{'name_first': 'test_fname', 'name_last': 'test_lname', 'u_id': 1}], 'name': 'test_ch_2'}]} and r.status_code == 200 