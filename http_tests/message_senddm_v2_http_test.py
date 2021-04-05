import pytest
import requests
import json
from src import config
import flask 

def test_long_message_send():
    requests.delete(config.url + 'clear/v1')

    #owner of dm/caller of dm_create
    reg_data = {
        'email': 'test_auth@gmail.com',
        'password': 'test_pw_auth',
        'name_first': 'testf',
        'name_last': 'testl'
    }

    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')
    #create one user to pass in the list of users for dm create
    reg_data2 = {
        'email': 'test_second@gmail.com',
        'password': 'test_pw_second',
        'name_first': 'secondf',
        'name_last': 'secondl'
    }
    r = requests.post(config.url + 'auth/register/v2', json=reg_data2)
    u_id2 = r.json().get('auth_user_id')

    create_data = {
        'token': token,
        'u_ids': [u_id2]
    }

    r = requests.post(config.url + 'dm/create/v1', json=create_data)
    dm_id = r.json().get('dm_id')

    # Testing sending message
    message = 'a' * 1001
    message_data = {'token': token, 'dm_id': dm_id, 'message': message}
    r = requests.post(config.url + 'message/senddm/v1', json=message_data)

    assert r.status_code == 404
