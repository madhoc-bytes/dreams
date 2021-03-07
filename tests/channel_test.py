import pytest

from src.data import users, channels
from src.auth import auth_register_v1
from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1


#General case for join

def test_join_channel():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel = channels_create_v1(test_user['auth_user_id'], "test channel", True)
    channel_join_v1(test_user, test_channel)
    details = channel_details_v1(test_user, test_channel)
    assert details['all_members'] == [
        {
            'u_id': test_user['auth_user_id'],
            'name_first': 'testF',
            'name_last': 'testL'
        }
    ]



#Pass an invalid uid

def test_join_invalid_uid():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel_id = channels_create_v1(test_user, "test channel", True)
    invalid = {'auth_user_id': 10}
    with pytest.raises(InputError):
        channel_join_v1(invalid, test_channel_id)


#Pass an invalid channel id

def test_join_invalid_channel_id():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    with pytest.raises(InputError):
        channel_join_v1(test_user, "invalid channel id")

'''
Call channel with no message
'''
def test_messages_nomessage():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel = channels_create_v1(test_user, "test channel", True)
    channel_join_v1(test_user, test_channel)
    assert channel_messages_v1(test_user, test_channel, 0) == {
        'messages': [],
        'start': 0,
        'end': -1,
    }

'''
Pass an invalid user id
'''
def test_channel_messages_invalid_uid():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel = channels_create_v1(test_user, "test channel", True)
    invalid = {'auth_user_id': 10}
    with pytest.raises(InputError):
        channel_messages_v1(invalid, test_channel, 0)

'''
Pass an invalid channel id
'''
def test_channel_messages_invalid_ch_id():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel = channels_create_v1(test_user, "test channel", True)
    invalid = {'id': 10}
    with pytest.raises(InputError):
        channel_messages_v1(test_user, invalid, 0)

'''
Start > total no. msgs in channel
'''
def test_channel_start_too_big():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_channel = channels_create_v1(test_user, "test channel", True)
    channel_join_v1(test_user, test_channel)
    with pytest.raises(InputError):
        channel_messages_v1(test_user, test_channel, 1)

'''
Passed user is not member of passed channel
'''
def test_messages_not_member():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "password", "testF", "testL")
    test_user2 = auth_register_v1("user@example.com", "password2", "testFF", "testLL")
    test_channel = channels_create_v1(test_user, "test channel", True)
    channel_join_v1(test_user, test_channel)
    with pytest.raises(AccessError):
        channel_messages_v1(test_user2, test_channel, 0)