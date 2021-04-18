import pytest
import requests
import json
from src import config
import flask
from src.error import InputError, AccessError
from datetime import datetime, timezone, timedelta

def test_message_sendlaterdm_basic():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    dm_data = {
        'token': token,
        'u_ids': [],
    }

    r = requests.post(config.url + 'dm/create/v1', json=dm_data)
    dm_id = r.json().get('dm_id')
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    sendlater_data = {
        'token': token,
        'dm_id': dm_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlaterdm/v1', json=sendlater_data)

    assert r.status_code == 200

def test_message_sendlaterdm_timeinpast():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    dm_data = {
        'token': token,
        'u_ids': [],
    }

    r = requests.post(config.url + 'dm/create/v1', json=dm_data)
    dm_id = r.json().get('dm_id')
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) - 1
    sendlater_data = {
        'token': token,
        'dm_id': dm_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlaterdm/v1', json=sendlater_data)

    assert r.status_code == 400

def test_message_sendlaterdm_invalid_dmid():
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
        'dm_id': 3,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlaterdm/v1', json=sendlater_data)

    assert r.status_code == 400

def test_message_sendlaterdm_longstring():
    requests.delete(config.url + 'clear/v1')

    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')

    dm_data = {
        'token': token,
        'u_ids': [],
    }

    r = requests.post(config.url + 'dm/create/v1', json=dm_data)
    dm_id = r.json().get('dm_id')

    long_string = "asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa"
    
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    sendlater_data = {
        'token': token,
        'dm_id': dm_id,
        'message': long_string,
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlaterdm/v1', json=sendlater_data)

    assert r.status_code == 400

def test_sendlaterdm_not_in_dm():
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

    dm_data = {
        'token': token1,
        'u_ids': [],
    }

    r = requests.post(config.url + 'dm/create/v1', json=dm_data)
    dm_id = r.json().get('dm_id')

    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    sendlater_data = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'string',
        'time_sent': time_sent,
    }

    r = requests.post(config.url + 'message/sendlaterdm/v1', json=sendlater_data)

    assert r.status_code == 403