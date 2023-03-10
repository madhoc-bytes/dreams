import pytest
import requests
import json
from src import config
import urllib


def test_basic():
    requests.delete(config.url + 'clear/v1')
    # register a user
    reg_data = {
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    }

    # acquire token and id of user
    resp_register = requests.post(config.url + 'auth/register/v2', json=reg_data)
    assert resp_register.status_code == 200
    # check for the length of the dictionary returned

def test_invalid_email():

    requests.delete(config.url + 'clear/v1')
    reg_data = {
        'email': 'thisisinvalid',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=reg_data)
    assert resp_register.status_code == 400

def test_auth_register_short_password():
    reg_data = {
        'email': 'abc@def.com',
        'password': 'A',
        'name_first': 'John',
        'name_last': 'Smith'
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=reg_data)
    assert resp_register.status_code == 400


def test_auth_register_short_first_name():
    data = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J',
        'name_last': 'Smith'
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=data)
    assert resp_register.status_code == 400

def test_auth_register_short_last_name():
    data = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=data)
    assert resp_register.status_code == 400

def test_auth_register_long_first_name():
    data = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'J'*52,
        'name_last': 'Smith'
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=data)
    assert resp_register.status_code == 400

def test_auth_register_long_last_name():
    data = {
        'email': 'abc@def.com',
        'password': 'Password01!',
        'name_first': 'John',
        'name_last': 'S'*52
    }

    resp_register = requests.post(config.url + 'auth/register/v2', json=data)
    assert resp_register.status_code == 400
    