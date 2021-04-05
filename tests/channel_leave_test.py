import pytest

from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_details_v2, channel_leave_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v2

def test_basic():
    clear_v2()

    # create user
    test_user = auth_register_v2("test@gmail.com", "password", "testF", "testL")

    # create channel
    test_channel = channels_create_v2(test_user['token'], "test channel", True)['channel_id']

    # add user to channel and check if successful
    channel_join_v2(test_user['token'], test_channel)
    details = channel_details_v2(test_user['token'], test_channel)
    assert details['all_members'] == [
        {
            'u_id': test_user['auth_user_id'],
            'name_first': 'testF',
            'name_last': 'testL'
        }
    ]

    # remove user from channel and check if channel is empty
    channel_leave_v2(test_user['token'], test_channel)
    assert details['all_members'] == []

def test_invalid_channel():
    clear_v2()
    # create user
    test_user = auth_register_v2("test@gmail.com", "password", "testF", "testL")

    # try to leave from non-existent channel and expect input error
    with pytest.raises(InputError):
        channel_leave_v2(test_user['token'], "invalid channel id")

def test_unauthorised_user():
    clear_v2()

    # register 1 user
    token = auth_register_v2(
        'test_auth@gmail.com',
        'test_pw_auth',
        'test_fname_auth',
        'test_lname_auth')['token']

    # create a test channel
    test_channel_id = channels_create_v2(token, 'test_channel_1', True)['channel_id']

    # try to call channel_leave when auth_user is not in the channel and expect failure
    with pytest.raises(AccessError):
        channel_leave_v2(token, test_channel_id)