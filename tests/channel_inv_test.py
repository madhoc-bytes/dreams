import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError



def test_invite_basic():    
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com', 'test_pw_auth', 'test_fname_auth', 'test_lname_auth')
    invitee_id = auth_register_v1('test_user@gmail.com', 'test_pw_user', 'test_fname_user', 'test_lname_user')

    # create a test channel
    test_channel_id = channels_create_v1(auth_id, 'test_channel_1', True)


    # place inviter and invitee into test channel  
    channel_join_v1(auth_id, test_channel_id)
    channel_invite_v1(auth_id, 'test_channel_id', invitee_id)

    test_ch_details = channel_details_v1(auth_id, test_channel_id)
    assert test_ch_details['all_members'] == [
        {
            'u_id': auth_id, 
            'name_first': 'test_fname_auth', 
            'name_last': 'test_lname_auth'
        },
        {
            'u_id': invitee_id, 
            'name_first': 'test_fname_user', 
            'name_last': 'test_lname_user'
        },
    ]

def test_invite_channel_invalid():
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com', 'test_pw_auth', 'test_fname_auth', 'test_lname_auth')
    invitee_id = auth_register_v1('test_user@gmail.com', 'test_pw_user', 'test_fname_user', 'test_lname_user')

    # try to add them to a non-existent channel and expect failure
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, "test invalid id", invitee_id)

def test_invite_user_invalid():
    clear_v1()

    # register 1 user
    auth_id = auth_register_v1('test_auth@gmail.com', 'test_pw_auth', 'test_fname_auth', 'test_lname_auth')

    # create a test channel
    test_channel_id = channels_create_v1(auth_id, 'test_channel_1', True)

    # place inviter into test channel  
    channel_join_v1(auth_id, test_channel_id)

    # try to add non-existent user to channel and expect failure
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, "test invalid id", "non_existent_u_id")


def test_invite_inviter_not_in_channel():    
    clear_v1()

    # register 2 users
    auth_id = auth_register_v1('test_auth@gmail.com', 'test_pw_auth', 'test_fname_auth', 'test_lname_auth')
    invitee_id = auth_register_v1('test_user@gmail.com', 'test_pw_user', 'test_fname_user', 'test_lname_user')

    # create a test channel
    test_channel_id = channels_create_v1(auth_id, 'test_channel_1', True)

    # try to invite users to channel when inviter is not in channel and expect failure
    with pytest.raises(AccessError):
        channel_invite_v1(auth_id, 'test_channel_id', invitee_id)

