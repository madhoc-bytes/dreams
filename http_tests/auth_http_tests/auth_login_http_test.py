import urllib
import flask
import json 
import pytest
import requests
import urllib.request

def test_valid_login():
    
    data_register = json.dumps({
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        })
    data_login = json.dumps({
        'email': 'abc@def.com'
        'password': 'Password01!'
    })
    resp_register = requests.post(config.url + 'auth/register/v2', data=data_register, methods='POST')
    resp_login = requests.post(config.url + 'auth/login/v2', data=data_login, methods='POST')
    assert resp_login.status_code == 200
    assert resp_login['token'] == str(jwt.encode({resp_login['u_id']}, da.SECRET, algorithm='HS256'))

def test_invalid_email_login():

    data_register = json.dumps({
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        })
    data_login = json.dumps({
        'email': 'thisisinvalid'
        'password': 'Password01!'
    })
    resp_register = requests.post(config.url + 'auth/register/v2', data=data_register, methods='POST')
    resp_login = requests.post(config.url + 'auth/login/v2', data=data_login, methods='POST')
    assert resp_login.status_code == 400

def test_unused_email_login():

    data_register = json.dumps({
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        })
    data_login = json.dumps({
        'email': 'def@ghi.com'
        'password': 'Password01!'
    })
    resp_register = requests.post(config.url + 'auth/register/v2', data=data_register, methods='POST')
    resp_login = requests.post(config.url + 'auth/login/v2', data=data_login, methods='POST')
    assert resp_login.status_code == 400

def test_incorrect_password_login():

    data_register = json.dumps({
            'email': 'abc@def.com',
            'password': 'Password01!',
            'name_first': 'John',
            'name_last': 'Smith'
        })
    data_login = json.dumps({
        'email': 'def@ghi.com'
        'password': 'Password1122@'
    })
    resp_register = requests.post(config.url + 'auth/register/v2', data=data_register, methods='POST')
    resp_login = requests.post(config.url + 'auth/login/v2', data=data_login, methods='POST')
    assert resp_login.status_code == 400

