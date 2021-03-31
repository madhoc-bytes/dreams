import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v2
from src.other import clear_v1
from src.error import InputError, AccessError

def test_invite_basic():    
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']
    invitee_id = auth_register_v1('test_user@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(auth_id, 'test_channel_1', True)['channel_id']

    # place inviter and invitee into test channel  
    channel_join_v1(auth_id, test_channel_id)
    channel_invite_v1(auth_id, test_channel_id, invitee_id)

    test_ch_details = channel_details_v1(auth_id, test_channel_id)
    assert test_ch_details['all_members'] == [
        {             
            'name_first': 'test_fname_auth', 
            'name_last': 'test_lname_auth',
            'u_id': auth_id,
        },
        {             
            'name_first': 'test_fname_user', 
            'name_last': 'test_lname_user',
            'u_id': invitee_id,
        },
    ]

def test_invite_multiple():    
    clear_v1()

    # register 3 users
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']
    invitee_id = auth_register_v1('test_user@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['auth_user_id']
    invitee_id1 = auth_register_v1('test_user1@gmail.com',
    'test_pw_user1',
    'test_fname_user1',
    'test_lname_user1')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(auth_id, 'test_channel_1', True)['channel_id']

    # place inviter test channel  
    channel_join_v1(auth_id, test_channel_id)

    # invite 2 users
    channel_invite_v1(auth_id, test_channel_id, invitee_id)
    channel_invite_v1(auth_id, test_channel_id, invitee_id1)

    test_ch_details = channel_details_v1(auth_id, test_channel_id)
    assert test_ch_details['all_members'] == [
        {             
            'name_first': 'test_fname_auth', 
            'name_last': 'test_lname_auth',
            'u_id': auth_id,
        },
        {             
            'name_first': 'test_fname_user', 
            'name_last': 'test_lname_user',
            'u_id': invitee_id,
        },
        {             
            'name_first': 'test_fname_user1', 
            'name_last': 'test_lname_user1',
            'u_id': invitee_id1,
        },
    ]



def test_invite_channel_invalid():
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']
    invitee_id = auth_register_v1('test_user@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['auth_user_id']

    # try to invite 1 to a non-existent channel and expect failure
    invalid_channel_id = 100
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, invalid_channel_id, invitee_id)


def test_invite_user_invalid():
    clear_v1()

    # register 1 user
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(auth_id, 'test_channel_1', True)['channel_id']

    # place inviter into test channel  
    channel_join_v1(auth_id, test_channel_id)

    # try to add non-existent user to channel and expect failure
    invalid_user_id = 100
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, test_channel_id, invalid_user_id)


def test_invite_inviter_not_in_channel():    
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com',
    'test_pw_auth',
    'test_fname_auth',
    'test_lname_auth')['auth_user_id']
    invitee_id = auth_register_v1('test_user@gmail.com',
    'test_pw_user',
    'test_fname_user',
    'test_lname_user')['auth_user_id']

    # create a test channel
    test_channel_id = channels_create_v2(auth_id, 'test_channel_1', True)['channel_id']

    # try to invite users to channel when inviter is not in channel and expect failure
    with pytest.raises(AccessError):
        channel_invite_v1(auth_id, test_channel_id, invitee_id)

