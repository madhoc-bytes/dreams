import pytest

from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError


def test_details_basic():    
    clear_v1()

    # register 1 user
    auth_token = auth_register_v2('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_user',
    'test_lname_user')['token']

    # create a test channel
    test_channel_id = channels_create_v2(auth_token, 'test_channel_1', True)['channel_id']

    # add auth to the test channel
    channel_join_v2(auth_token, test_channel_id)

    # retrieve details
    channel_dict = channel_details_v2(auth_token, test_channel_id)

    # ensure the info returned is correct
    assert channel_dict['name'] == 'test_channel_1'
    assert channel_dict['all_members'] == [
        {
            'u_id': 0,
            'token' = auth_token,
            'name_first': 'test_fname_user',
            'name_last': 'test_lname_user',
        }
    ]

def test_details_multiple ():    
    clear_v1()
    
    # register 2 users
    # register 2 users
    token1 = auth_register_v2('test_auth@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['token']
    token2 = auth_register_v2('test_user@gmail.com',
    'test_pw_user1',
    'test_fname_user1',
    'test_lname_user1')['token']


    # create a test channel
    test_channel_id = channels_create_v2(token1, 'test_channel_1', True)['channel_id']

    # add both to the test channel
    channel_join_v2(token1, test_channel_id)
    channel_join_v2(token2, test_channel_id)

    # retrieve details
    channel_dict = channel_details_v2(token1, test_channel_id)

    # ensure the info returned is correct
    assert channel_dict['name'] == 'test_channel_1'
    assert channel_dict['all_members'] == [
        {
            'u_id': 0,
            'token' = token1,
            'name_first': 'test_fname_user',
            'name_last': 'test_lname_user',
        },
        {
            'u_id': 1,
            'token' = token2,
            'name_first': 'test_fname_user1',
            'name_last': 'test_lname_user1',
        }
    ]

def test_invalid_channel():
    clear_v1()

    # register a user
    token = auth_register_v2('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['token']

    #try to recall details of a non-existent channel and expect failure
    invalid_channel_id = 100
    with pytest.raises(InputError):
        channel_details_v2(token, invalid_channel_id)

def test_unauthorised_user():
    clear_v1()

    # register 1 user
    token = auth_register_v2('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['token']

    # create a test channel
    test_channel_id = channels_create_v2(token, 'test_channel_1', True)['channel_id']

    # try to call channel_details when auth_user is not in the channel and expect failure
    with pytest.raises(AccessError):
        channel_details_v2(token, test_channel_id)

