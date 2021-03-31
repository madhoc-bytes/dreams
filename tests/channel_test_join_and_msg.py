'''Import pytest and relevant functions'''
import pytest

from src.auth import auth_register_v1
from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1

def test_join_channel():
    ''' General working case for joining'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_channel = channels_create_v2(test_user, "test channel", True)['channel_id']
    channel_join_v1(test_user, test_channel)
    details = channel_details_v1(test_user, test_channel)
    assert details['all_members'] == [
        {
            'u_id': test_user,
            'name_first': 'testF',
            'name_last': 'testL'
        }
    ]

def test_join_invalid_uid():
    '''Passing an invalid user id into join'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_channel_id = channels_create_v2(test_user, "test channel", True)['channel_id']
    invalid = 10
    with pytest.raises(InputError):
        channel_join_v1(invalid, test_channel_id)

def test_join_invalid_channel_id():
    '''Passing an inavlid channel id into join'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    with pytest.raises(InputError):
        channel_join_v1(test_user, "invalid channel id")

def test_messages_nomessage():
    '''Call messages given a channel with no messages'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_channel = channels_create_v2(test_user, "test channel", True)['channel_id']
    channel_join_v1(test_user, test_channel)
    assert channel_messages_v1(test_user, test_channel, 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }

def test_messages_invalid_uid():
    '''Call messages given an invalid user id'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_channel = channels_create_v2(test_user, "test channel", True)['channel_id']
    invalid = 10
    with pytest.raises(InputError):
        channel_messages_v1(invalid, test_channel, 0)

def test_messages_invalid_ch_id():
    '''Call messages given an invalid channel id'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    invalid = 10
    with pytest.raises(InputError):
        channel_messages_v1(test_user, invalid, 0)

def test_messages_start_too_big():
    '''Call messages given a start > number of messages in channel'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_channel = channels_create_v2(test_user, "test channel", True)['channel_id']
    channel_join_v1(test_user, test_channel)
    with pytest.raises(InputError):
        channel_messages_v1(test_user, test_channel, 1)

def test_messages_not_member():
    '''Call messages given a user not a member of the channel'''
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")['auth_user_id']
    test_user2 = auth_register_v1("user@example.com", "password2", "testFF", "testLL")['auth_user_id']
    test_channel = channels_create_v2(test_user, "test channel", True)['channel_id']
    channel_join_v1(test_user, test_channel)
    with pytest.raises(AccessError):
        channel_messages_v1(test_user2, test_channel, 0)
