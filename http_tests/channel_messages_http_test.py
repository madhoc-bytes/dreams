import pytest
import requests
import json
from src import config
import flask 

def test_messages_nomessage():
    '''Call messages given a channel with no messages'''
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

    #get return value channel create
    payload = r.json()
    #get token
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': token, 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    #channel messages
    messages_params = json.dumps({'token': token, 'channel_id': ch_id, 'start': 0})
    r = requests.get(config.url + 'channel/messages/v2', params=messages_params, methods='GET')

    assert(r.status_code == 200)

def test_messages_invalid_ch_id():
    '''Call messages given an invalid channel id'''
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    #get return value of auth register 
    payload = r.json()
    #get ch id
    token = payload['token']

    #channel messages
    messages_params = json.dumps({'token': token, 'channel_id': 10, 'start': 0})
    r = requests.get(config.url + 'channel/messages/v2', params=messages_params, methods='GET')

    assert(r.status_code == 400)

def test_messages_start_too_big():
    '''Call messages given a start > number of messages in channel'''
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
    #get return value channel create
    payload = r.json()
    #get ch id
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': token, 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')
    
    #channel messages
    messages_params = json.dumps({'token': token, 'channel_id': ch_id, 'start': 10})
    r = requests.get(config.url + 'channel/messages/v2', params=messages_params, methods='GET')

    assert(r.status_code == 400)

def test_messages_not_member():
    '''Call messages given a user not a member of the channel'''
    #clear_v1()
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    #auth_register_v1 first user
    data = json.dumps({'email': 'test@gmail.com', 'password': 'password', 'name_first': 'testF', 'name_last': 'testL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    #get return value of auth register 
    payload = r.json()
    #get token of first user
    token1 = payload['token']

    #auth_register_v1 second user
    data = json.dumps({'email': 'test2@gmail.com', 'password': 'password2', 'name_first': 'testFF', 'name_last': 'testLL'})
    r = requests.post(config.url + 'auth/register/v2', data=details, methods='POST')
    #get return value of auth register 
    payload = r.json()
    #get token
    token2 = payload['token']

    #channel create
    channel_data = json.dumps({'token': token, 'name': 'test channel', 'is_public': True})
    r = requests.post(config.url + 'channels/create/v2', data=create_data, methods='POST')
    #get return value channel create
    payload = r.json()
    #get ch id
    ch_id = payload['id']

    #channel join
    join_data = json.dumps({'token': token, 'channel_id': ch_id]})
    r = requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    #channel messages
    messages_params = json.dumps({'token': token2, 'channel_id': ch_id, 'start': 0})
    r = requests.get(config.url + 'channel/messages/v2', params=messages_data, methods='GET')

    assert(r.status_code == 500)
