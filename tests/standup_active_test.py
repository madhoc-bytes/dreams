import pytest
from src.channels import channels_create_v2 
from src.other import clear_v2
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.standup import standup_active_v1

def test_standup_active_invalidchannel_id():
    #clear_v2
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'Dyu', 'Baidas')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create the channel.
    channel_user1_id = channels_create_v2(user1_token, 'gitb' , True).get('channel_id')

    channel_item = channel_user1_id + 1
    with pytest.raises(InputError):
        standup_active_v1(user1_token, channel_item)
