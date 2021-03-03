import pytest

from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError


def test_details_basic():    
    clear_v1()

    # register 1 user
    auth_id = auth_register_v1('test_user@gmail.com', 'test_pw_user', 'test_fname_user', 'test_lname_user')

    # create a test channel
    test_channel_id = channels_create_v1(auth_id, 'test_channel_1', True)

    # add auth to the test channel
    channel_join_v1(auth_id, test_channel_id)

    # retrieve details
    channel_dict = channel_details_v1(auth_id, test_channel_id)

    # ensure the info returned is correct
    assert channel_dict['name'] == 'test_channel_1'
    assert channel_dict['all_members'] == [
        {
                'u_id': 0,
                'name_first': 'test_fname_user',
                'name_last': 'test_lname_user',
        }
    ]
    
    def test_invalid_channel():
        clear_v1()

        # register a user
        auth_id = auth_register_v1('test_auth@gmail.com', 'test_pw_auth', 'test_fname_auth', 'test_lname_auth')

        #try to recall details of a non-existent channel and expect failure
        invalid_channel_id = 100
        with pytest.raises(InputError):
            channel_details_v1(auth_id, invalid_channel_id);
    
    def test_unauthorised_user():
        clear_v1()

        # register 1 user
        auth_id = auth_register_v1('test_user@gmail.com', 'test_pw_user', 'test_fname_user', 'test_lname_user')

        # create a test channel
        test_channel_id = channels_create_v1(auth_id, 'test_channel_1', True)

        # try to call channel_details when auth_user is not in the channel and expect failure
        with pytest.raises(AccessError):
            channel_details_v1(auth_id, test_channel_id)

