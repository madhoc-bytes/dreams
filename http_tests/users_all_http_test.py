import pytest
import requests
import json
from src import config

def test_system():
    requests.delete(config.url + 'clear/v1')

    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token of user
    r = requests.post(config.url + 'auth/register/v2', json=reg_data)
    token = r.json().get('token')


    users_all_params = {'token' : token}
    r = requests.get(config.url + 'users/all/v1', params=users_all_params)
    assert r.status_code == 200