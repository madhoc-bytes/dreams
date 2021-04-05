import pytest

from src.auth import auth_register_v2
from src.channel import channel_addowner_v2, channel_details_v2, channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError

def test_basic():    
    clear_v2()

    # register 1 user
    user = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_user',
        'test_lname_user'
    )

    # create a test channel
    test_channel_id = channels_create_v2(
        user['token'],
        'test_channel_1',
        True)['channel_id']

    # add auth to the test channel
    channel_join_v2(user['token'], test_channel_id)

    # make user an owner
    channel_addowner_v2(user['token'], test_channel_id, user['auth_user_id'])

    # retrieve details
    details = channel_details_v2(user['token'], test_channel_id)

    assert details['owner_members'] == [
        {
            'u_id': 0,
            'name_first': 'test_fname_user',
            'name_last': 'test_lname_user',
        }
    ]

def test_invalid_channel():
    clear_v2()

    # register a user
    user = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )

    # try to recall details of a non-existent channel and expect failure
    invalid_channel_id = 10
    with pytest.raises(InputError):
        channel_addowner_v2(user['token'], invalid_channel_id, user['auth_user_id'])

def test_already_owner():
    clear_v2()

    # register 1 user
    user = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_user',
        'test_lname_user'
    )

    # create a test channel
    test_channel_id = channels_create_v2(
        user['token'],
        'test_channel_1',
        True)['channel_id']

    # add auth to the test channel
    channel_join_v2(user['token'], test_channel_id)

    # make user an owner
    channel_addowner_v2(user['token'], test_channel_id, user['auth_user_id'])    
    
    with pytest.raises(InputError):
        channel_addowner_v2(user['token'], test_channel_id, user['auth_user_id'])

def test_no_privileges():
    clear_v2()
    
    # register 2 users. first one will be the owner of Dreams
    user1 = auth_register_v2(
        'test_auth1@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )
    user2 = auth_register_v2(
        'test_user@gmail.com',
        'test_pw_user',
        'test_fname_user',
        'test_lname_user'
    )

    # create a test channel
    test_channel_id = channels_create_v2(
        user1['token'],
        'test_channel_1',
        True)['channel_id']

    # add both users to the test channel
    channel_join_v2(user1['token'], test_channel_id)
    channel_join_v2(user2['token'], test_channel_id)

    # try to let non-owner (user2) make user1 an owner and expect failure
    with pytest.raises(InputError):
        channel_addowner_v2(user2['token'], test_channel_id, user1['auth_user_id'])