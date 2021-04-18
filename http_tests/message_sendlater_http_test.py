import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError
from datetime import datetime, timezone, timedelta

def test_message_sendlater_basic():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

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
    r = requests.post(config.url + 'channel/join/v2', json=join_data)
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    sendlater_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlater/v1', json=sendlater_data)

    assert r.status_code == 200

def test_message_sendlater_timeinpast():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

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
    r = requests.post(config.url + 'channel/join/v2', json=join_data)
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) - 1

    sendlater_data = {
        'token': token,
        'channel_id': ch_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlater/v1', json=sendlater_data)

    assert r.status_code == 400

def test_message_sendlater_invalid_ch():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    sendlater_data = {
        'token': token,
        'channel_id': 1,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlater/v1', json=sendlater_data)

    assert r.status_code == 400

def test_message_sendlater_longmsg():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

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
    r = requests.post(config.url + 'channel/join/v2', json=join_data)
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    long_string = "asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa"
    sendlater_data = {
        'token': token,
        'channel_id': ch_id,
        'message': long_string,
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlater/v1', json=sendlater_data)

    assert r.status_code == 400

def test_message_sendlater_notinch():
    requests.delete(config.url + 'clear/v1')

    reg_data1 = {
        'email': 'test_1@gmail.com',
        'password': 'test_pw_1',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data1)
    token1 = r.json().get('token')

    reg_data2 = {
        'email': 'test_2@gmail.com',
        'password': 'test_pw_2',
        'name_first': 'testff',
        'name_last': 'testll'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    token2 = r.json().get('token')

    ch_data = {
        'token': token1,
        'name': 'test_ch',
        'is_public': True
    }

    # acquire channel id
    r = requests.post(config.url + 'channels/create/v2', json=ch_data)
    ch_id = r.json().get('channel_id')

    # join user to channel
    join_data = {
        'token': token1,
        'channel_id': ch_id
    }   
    r = requests.post(config.url + 'channel/join/v2', json=join_data)
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1

    sendlater_data = {
        'token': token2,
        'channel_id': ch_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlater/v1', json=sendlater_data)

    assert r.status_code == 403