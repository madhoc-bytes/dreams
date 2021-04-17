import pytest

from datetime import datetime, timezone
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.message import message_send_v1
from src.dm import dm_create_v1
from src.search import search_v2
from src.message_senddm_v2 import message_senddm_v2
from src.error import InputError, AccessError
from src.other import clear_v2

from src.user import user_stats_v1

def test_system():
    clear_v2()

    # register 1 user
    user1 = auth_register_v2(
        'test_user1@gmail.com',
        'test_pw_user1',
        'test_fname_user1',
        'test_lname_user1')

    # create a test channel
    test_channel_id = channels_create_v2(user1['token'], 'test_channel_1', True)['channel_id']

    # add user to the test channel
    channel_join_v2(user1['token'], test_channel_id)
    
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())

    # check timestamp
    assert user_stats_v1(user1['token'])['user_stats']['channels_joined'][user1['auth_user_id']]['time_stamp'] == time_now
    
    # check other info of user
    assert len(user_stats_v1(user1['token'])['user_stats']['channels_joined']) == 1
    assert len(user_stats_v1(user1['token'])['user_stats']['dms_joined']) == 0
    assert len(user_stats_v1(user1['token'])['user_stats']['messages_sent']) == 0
    assert user_stats_v1(user1['token'])['user_stats']['involvement_rate'] == 1

    # register another user
    user2 = auth_register_v2(
        'test_user2@gmail.com',
        'test_pw_user2',
        'test_fname_user2',
        'test_lname_user2')
    
    dm_id = dm_create_v1(user1['token'], [user2['auth_user_id']])['dm_id']

    # check if their joining of the dm was recorded
    assert len(user_stats_v1(user1['token'])['user_stats']['dms_joined']) == 1
    assert len(user_stats_v1(user2['token'])['user_stats']['dms_joined']) == 1

    # check the timestamp again
    time_now2 = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    assert user_stats_v1(user1['token'])['user_stats']['dms_joined'][user1['auth_user_id']]['time_stamp'] == time_now2
    
    # check if messages sent are updating
    message_senddm_v2(user1['token'], dm_id, "test_message_dm")
    assert len(user_stats_v1(user1['token'])['user_stats']['messages_sent']) == 1

    message_send_v1(user1['token'], test_channel_id, "test_message_ch")
    assert len(user_stats_v1(user1['token'])['user_stats']['messages_sent']) == 2

