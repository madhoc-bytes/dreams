import pytest
import requests
import json
from src import config
import flask

#server vreate test
def test_channels_create_httptest(url):
    data1 = {
        'email': "asdzxc3445@gmail.com", 
        'password': "askldfb",
        'name_first': "Baida", 
        'name_last': "Du",
    }
    r = requests.post(f"{url}/auth/register", json=data1)
    channels_http_return = r.json()
    resp = requests.post(f"{url}/channels/create", json={'token': channels_http_return['token'], 'name': 'first', 'is_public': True}) 
    assert resp.json() == {'channel_id' : 0}
    resp = requests.post(f"{url}/channels/create", json={'token': channels_http_return['token'], 'name': 'second', 'is_public': True}) 
    assert resp.json() == {'channel_id' : 1}