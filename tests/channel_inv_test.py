import pytest

from src.auth import auth_register_v2
from src.channel import channel_invite_v2, channel_details_v2, channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError

def test_invite_basic():    
    clear_v2()

    # register 2 users
    auth_id = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )
    invitee_id = auth_register_v2(
        'test_user@gmail.com',
        'test_pw_user',
        'test_fname_user',
        'test_lname_user'
    )

    # create a test channel
    test_channel_id = channels_create_v2(auth_id['token'], 'test_channel_1', True)['channel_id']

    # place inviter and invitee into test channel  
    channel_join_v2(auth_id['token'], test_channel_id)
    channel_invite_v2(auth_id['token'], test_channel_id, invitee_id['auth_user_id'])

    test_ch_details = channel_details_v2(auth_id['token'], test_channel_id)
    assert test_ch_details['all_members'] == [
        {             
            'name_first': 'test_fname_auth', 
            'name_last': 'test_lname_auth',
            'u_id': auth_id['auth_user_id'],
        },
        {             
            'name_first': 'test_fname_user', 
            'name_last': 'test_lname_user',
            'u_id': invitee_id['auth_user_id'],
        }
    ]

def test_invite_multiple():    
    clear_v2()

    # register 3 users
    auth_id = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )
    invitee_id = auth_register_v2(
        'test_user@gmail.com',
        'test_pw_user',
        'test_fname_user',
        'test_lname_user'
        )
    invitee_id1 = auth_register_v2(
        'test_user1@gmail.com',
        'test_pw_user1',
        'test_fname_user1',
        'test_lname_user1'
    )

    # create a test channel
    test_channel_id = channels_create_v2(auth_id['token'], 'test_channel_1', True)['channel_id']

    # place inviter test channel  
    channel_join_v2(auth_id['token'], test_channel_id)

    # invite 2 users
    channel_invite_v2(auth_id['token'], test_channel_id, invitee_id['auth_user_id'])
    channel_invite_v2(auth_id['token'], test_channel_id, invitee_id1['auth_user_id'])

    test_ch_details = channel_details_v2(auth_id['token'], test_channel_id)
    assert test_ch_details['all_members'] == [
        {             
            'name_first': 'test_fname_auth', 
            'name_last': 'test_lname_auth',
            'u_id': auth_id['auth_user_id'],
        },
        {             
            'name_first': 'test_fname_user', 
            'name_last': 'test_lname_user',
            'u_id': invitee_id['auth_user_id'],
        },
        {             
            'name_first': 'test_fname_user1', 
            'name_last': 'test_lname_user1',
            'u_id': invitee_id1['auth_user_id'],
        },
    ]

def test_invite_channel_invalid():
    clear_v2()

    # register 2 users
    auth_id = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )
    invitee_id = auth_register_v2(
        'test_user@gmail.com',
        'test_pw_user',
        'test_fname_user',
        'test_lname_user'
    )

    # try to invite 1 to a non-existent channel and expect failure
    invalid_channel_id = 100
    with pytest.raises(InputError):
        channel_invite_v2(auth_id['token'], invalid_channel_id, invitee_id['auth_user_id'])

def test_invite_user_invalid():
    clear_v2()

    # register 1 user
    auth_id = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )

    # create a test channel
    test_channel_id = channels_create_v2(auth_id['token'], 'test_channel_1', True)['channel_id']

    # place inviter into test channel  
    channel_join_v2(auth_id['token'], test_channel_id)

    # try to add non-existent user to channel and expect failure
    invalid_user_id = 100
    with pytest.raises(InputError):
        channel_invite_v2(auth_id['token'], test_channel_id, invalid_user_id)

def test_invite_inviter_not_in_channel():    
    clear_v2()

    # register 2 users
    auth_id = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth'
    )
    invitee_id = auth_register_v2(
        'test_user@gmail.com',
        'test_pw_user',
        'test_fname_user',
        'test_lname_user'
    )

    # create a test channel
    test_channel_id = channels_create_v2(auth_id['token'], 'test_channel_1', True)['channel_id']

    # try to invite users to channel when inviter is not in channel and expect failure
    with pytest.raises(AccessError):
        channel_invite_v2(auth_id['token'], test_channel_id, invitee_id['auth_user_id'])

