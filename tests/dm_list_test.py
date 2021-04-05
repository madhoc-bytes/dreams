import pytest

from src.data import users, channels, dms
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_list_v1, dm_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v2

def test_dm_list_basic():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    
    assert(dm_list_v1(auth_token) == {'dms': []})


def test_dm_list_basic_onedm():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    
    u_ids = []
    dm_create_v1(auth_token, u_ids)
    assert(dm_list_v1(auth_token) == {'dms': [
        {
            'name': 'testftestl', 
            'members': [
            {
                'u_id': 0, 
                'name_first': 'testf', 
                'name_last': 'testl'
            }]
        }]
    })