import pytest
from src.channels import channels_create_v2 
from src.other import clear_v2
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.standup import standup_start_v1

def test_standup_start_invalidtoken():
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'Dyu', 'Baidas')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create the channel.
    channel_user1_id = channels_create_v2(user1_token, 'gitb' , True).get('channel_id')

    token_item = user1_token + ' '
    with pytest.raises(AccessError):
        standup_start_v1(token_item, channel_user1_id, 1)

def test_standup_start_invalidchannelid():
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'Dyu', 'Baidas')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create the channel.
    channel_user1_id = channels_create_v2(user1_token, 'gitb' , True).get('channel_id')

    channel_item = channel_user1_id + 1
    with pytest.raises(InputError):
        standup_start_v1(user1_token, channel_item, 1)

def test_standup_start_occpuy():
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'Dyu', 'Baidas')
    user1_token = user1['token']

    #create the channel.
    channel_user1_id = channels_create_v2(user1_token, 'gitb' , True)

    with pytest.raises(InputError):
        standup_start_v1(user1_token, channel_user1_id, 1)
