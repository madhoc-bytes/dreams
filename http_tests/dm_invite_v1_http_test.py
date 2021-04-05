# HTTP Test File for dm/invite/v1 

# Imports
import pytest
import requests
import json
from src import config
import flask
from error import InputError, AccessError

def test_dm_invite_one_user():
    # Reset
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # Register user 1
    register_data = {'email': 'germanijack@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token 1
    payload = r.json()
    token = payload['token']

    # Register user 2
    register_data = {'email': 'test@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token 2
    payload = r.json()
    token_2 = payload['token']

    user_id = token_to_id(token_2)

    # Register user 3
    register_data = {'email': 'test123@yahoo.com', 'password': 'jack123', 'name_first': 'Jack', 'name_last': 'Germani'}
    r = requests.post(config.url + 'auth/register/v2', data=register_data, methods='POST')
    
    # Get token 3
    payload = r.json()
    token_3 = payload['token']

    user_id_2 = token_to_id(token_3)

    # Create DM
    create_dm_data = {'token': token, 'u_ids': user_id}
    r = requests.post(config.url + 'dm/create/v1', data=create_dm_data, methods='POST')

    # Get DM id
    payload = r.json()
    dm_id = payload['dm_id']

    requests.post(config.url + 'dm/invite/v1', data=share_id, methods='POST')

    assert resp.status_code == 200

