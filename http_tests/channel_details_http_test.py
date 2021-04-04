import pytest
import requests
import json
from src import config

def test_valid():
    requests.delete(config.url + 'clear/v2', methods='DELETE')

    # register a user
    reg_data = json.dumps({
        'email': 'test@gmail.com',
        'password': 'testpw123',
        'name_first': 'test_fname',
        'name_last': 'test_lname'
    })
    r = requests.post(config.url + 'auth/register/v2', data=reg_data, methods='POST')

    # acquire token
    payload = r.json()    
    token = payload['token']
    
    # create a channel
    ch_data = json.dumps({
        'token': token,
        'name': 'test_ch',
        'is_public': True
    })    
    r = requests.post(config.url + 'channels/create', data=ch_data, methods='POST')    
    
    # acquire channel id
    payload = r.json()
    ch_id = payload['id']

    # add user to channel
    join_data = json.dumps({
        'token': token,
        'channel_id': ch_id
    })    
    requests.post(config.url + 'channel/join/v2', data=join_data, methods='POST')

    details_params = {
        'token': token,
        'channel_id': ch_id
    }
    # testing channel details v2
    # join_data will provide the right input for channel details as well
    r = requests.get(config.url + 'channel/details/v2', params=details_params, methods='GET')
    assert json.loads(r.text) == {
        'name': 'test_ch',
        'is_public' : True,
        'owner_members' : []
        'all_members' : [
            {
                'u_id': 0,
                'name_first': 'test_fname',
                'name_last': 'test_lname',
            }
        ]
    }

