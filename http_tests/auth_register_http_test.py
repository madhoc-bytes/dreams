import urllib
import flask
import json 
import pytest
import requests
import urllib.request
from src import config
from src.auth import auth_register_v2


def test_valid_register():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp = requests.post(config.url + 'auth/register/v2', data=data)
    assert resp.status_code == 200
    # check for the length of the dictionary returned 

'''
def test_invalid_email():
    data = json.dumps({
        'email': 'thisisinvalid',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    resp = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400

def test_auth_register_short_password():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'A',
        'name_first': 'John',
        'name_last': 'Smith'
    })

    req = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400

def test_auth_register_short_first_name():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J',
        'name_last': 'Smith'
    })

    req = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400

def test_auth_register_short_last_name():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'
    })

    req = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400

def test_auth_register_long_first_name():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J'*52,
        'name_last': 'Smith'
    })

    req = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400

def test_auth_register_long_last_name():
    data = json.dumps({
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'*52
    })

    req = requests.post(config.url + 'auth/register', data=data)
    assert resp.status_code == 400
'''