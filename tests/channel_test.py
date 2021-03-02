import pytest

from src.auth import auth_register_v1
from src.channel import channel_messages_v1, channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1


'''
General case for join
'''
def test_join_channel():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "test", "testF", "testL")
    test_channel = channels_create_v1(test, "test channel", True)   
    channel_join_v1(test_user, test_channel)
    details = channel_details_v1(test_user, test_channel)
    assert details['all_members'] == [{'u_id': test_user, 'name_first': 'testF', 'name_last': 'testL'}]


'''
Pass an invalid uid
'''
def test_join_invalid_uid():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "test", "testF", "testL")
    test_channel_id = channels_create_v1(test, "test channel", True)
    with pytest.raises(InputError):
        channel_join_v1("test invalid", test_channel_id)

'''
Pass an invalid channel id
'''
def test_join_invalid_channel_id():
    clear_v1()
    test_user = auth_register_v1("test@gmail.com", "test", "testF", "testL")
    test_channel_id = channels_create_v1(test, "test channel", True)
    with pytest.raises(InputError):
        channel_join_v1(test_user, "invalid channel id")


