import pytest

from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError


def test_details_basic():    
    clear_v1()

    # register 1 user
    user = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_user',
    'test_lname_user')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(user, 'test_channel_1', True)['channel_id']

    # add auth to the test channel
    channel_join_v1(user, test_channel_id)

    # retrieve details
    channel_dict = channel_details_v1(user, test_channel_id)

    # ensure the info returned is correct
    assert channel_dict['name'] == 'test_channel_1'
    assert channel_dict['all_members'] == [
        {
                'u_id': 0,
                'name_first': 'test_fname_user',
                'name_last': 'test_lname_user',
        }
    ]

def test_details_multiple ():    
    clear_v1()
    
    # register 2 users
    # register 2 users
    user1 = auth_register_v1('test_auth@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['auth_user_id']
    user2 = auth_register_v1('test_user@gmail.com',
    'test_pw_user1',
    'test_fname_user1',
    'test_lname_user1')['auth_user_id']


    # create a test channel
    test_channel_id = channels_create_v2(user1, 'test_channel_1', True)['channel_id']

    # add both to the test channel
    channel_join_v1(user1, test_channel_id)
    channel_join_v1(user2, test_channel_id)

    # retrieve details
    channel_dict = channel_details_v1(user1, test_channel_id)

    # ensure the info returned is correct
    assert channel_dict['name'] == 'test_channel_1'
    assert channel_dict['all_members'] == [
        {
                'u_id': 0,
                'name_first': 'test_fname_user',
                'name_last': 'test_lname_user',
        },
        {
                'u_id': 1,
                'name_first': 'test_fname_user1',
                'name_last': 'test_lname_user1',
        }
    ]

def test_invalid_channel():
    clear_v1()

    # register a user
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']

    #try to recall details of a non-existent channel and expect failure
    invalid_channel_id = 100
    with pytest.raises(InputError):
        channel_details_v1(auth_id, invalid_channel_id)

def test_unauthorised_user():
    clear_v1()

    # register 1 user
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(auth_id, 'test_channel_1', True)['channel_id']

    # try to call channel_details when auth_user is not in the channel and expect failure
    with pytest.raises(AccessError):
        channel_details_v1(auth_id, test_channel_id)

