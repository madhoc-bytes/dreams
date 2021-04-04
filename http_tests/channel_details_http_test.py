import pytest
import requests
import json
from src import config

def test_valid():
    # requests.delete(config.url + 'clear/v2', methods='DELETE')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })
    r = requests.post(config.url + 'auth/register/v2', data=reg_data)

    # acquire token  
    token = r.json.get('token')

    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })    
    r = requests.post(config.url + 'channels/create', data=ch_data)    
    
    # acquire channel id    
    ch_id = r.json.get('id')

    # add user to channel
    join_data = json.dumps({
        'token': token,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data)

    details_params = {
        'token': token,
        'channel_id': ch_id
    }
    # testing channel details v2
    # join_data will provide the right input for channel details as well
    r = requests.get(config.url + 'channel/details/v2', params=details_params)
    assert r.status_code == 200

