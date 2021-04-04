import pytest
import requests
import json
from src import config
import flask 

def test_join_channel():
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    
    #get return value of auth register 
    payload = r.json()
    #get token
    token = payload['token']
    
    #channel create
    channel_data = json.dumps({'token': token, 'name': 'test channel', 'is_public': True})
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    
    #get return value of channel create
    payload = r.json()
    #get channel id
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': token, 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    #channel details
    details_params = json.dumps({'token': token, 'channel_id': ch_id})
    r = requests.get(config.url + 'channel/details/v2', params=details_params, methods='GET')

    assert(r.status_code == 200)

def test_join_invalid_uid():
    '''Passing an invalid user id into join'''
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    
    #get return value of auth register 
    payload = r.json()
    #get token
    token = payload['token']

    #channel create
    channel_data = json.dumps({'token': token, 'name': 'test channel', 'is_public': True})
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    #get return value of channel create
    payload = r.json()
    #get channel id
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': 'invalidtoken', 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    assert(r.status_code == 400)

def test_join_invalid_channel_id():
    '''Passing an inavlid channel id into join'''
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    
    #get return value of auth register 
    payload = r.json()
    #get token
    token = payload['token']

    #channel join
    join_data = json.dumps({'token': token, 'channel_id': 'invalid ch id']})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    assert(r.status_code == 400)

def test_join_private():
    '''Passing an invalid user id into join'''
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    
    #get return value of auth register 
    payload = r.json()
    #get token
    token = payload['token']

    #channel create
    channel_data = json.dumps({'token': token, 'name': 'test channel', 'is_public': False)
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    #get return value of channel create
    payload = r.json()
    #get channel id
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': 'invalidtoken', 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    assert(r.status_code == 500)