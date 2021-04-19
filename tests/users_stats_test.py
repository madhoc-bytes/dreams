import pytest

from datetime import datetime, timezone
import time
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.message import message_send_v1, message_remove_v1
from src.dm import dm_create_v1, dm_remove_v1
from src.search import search_v2
from src.message_senddm_v2 import message_senddm_v2
from src.error import InputError, AccessError
from src.other import clear_v2

from src.users import users_stats_v1

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
    
    # check timestamp
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    assert users_stats_v1(user1['token'])['dreams_stats']['channels_exist'][test_channel_id]['time_stamp'] == time_now
    
    # check other info of dreams
    assert len(users_stats_v1(user1['token'])['dreams_stats']['channels_exist']) == 1
    assert len(users_stats_v1(user1['token'])['dreams_stats']['dms_exist']) == 0
    assert len(users_stats_v1(user1['token'])['dreams_stats']['messages_exist']) == 0
    
    # register another user
    user2 = auth_register_v2(
        'test_user2@gmail.com',
        'test_pw_user2',
        'test_fname_user2',
        'test_lname_user2')
    
    # delay execution to check timestamp 
    time.sleep(0.1)

    # create a dm
    dm_id = dm_create_v1(user1['token'], [user2['auth_user_id']])['dm_id']

    # check the timestamp of dms now
    time_now2 = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    assert users_stats_v1(user1['token'])['dreams_stats']['dms_exist'][dm_id]['time_stamp'] == time_now2

    # check if the dm timestamp updated
    assert len(users_stats_v1(user1['token'])['dreams_stats']['dms_exist']) == 1
    
    # send dm msg and ch msg check if timestamps are recorded
    msg_id1 = message_senddm_v2(user1['token'], dm_id, "test_message_dm")['message_id']
    assert len(users_stats_v1(user1['token'])['dreams_stats']['messages_exist']) == 1

    msg_id2 = message_send_v1(user1['token'], test_channel_id, "test_message_ch")['message_id']
    assert len(users_stats_v1(user1['token'])['dreams_stats']['messages_exist']) == 2

    # remove both and check if there are 4 timestamps
    message_remove_v1(user1['token'], msg_id1)
    message_remove_v1(user1['token'], msg_id2)
    assert len(users_stats_v1(user1['token'])['dreams_stats']['messages_exist']) == 4

    #remove dm and check if there are timestamps for creation and deletion
    dm_remove_v1(user1['token'], dm_id)
    assert len(users_stats_v1(user1['token'])['dreams_stats']['dms_exist']) == 2