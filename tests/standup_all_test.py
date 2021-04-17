import pytest
from src.channels import channels_create_v2 
from src.other import clear_v2
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError, AccessError
from src.standup import standup_active_v1, standup_start_v1, standup_send_v1

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
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create the channel.
    channel_user1_id = channels_create_v2(user1_token, 'gitb' , True).get('channel_id')

    with pytest.raises(InputError):
        standup_start_v1(user1_token, channel_user1_id, 1)

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

def test_standup_active():
    #clear
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'Dyu', 'Baidas')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create two channels 
    channel_user1_id = channels_create_v2(user1_token,'gitb',True).get('channel_id')
    channel_user2_id = channels_create_v2(user1_token,'gitb2',True).get('channel_id')

    #start a standup 
    standup_1 = standup_start_v1(user1_token, channel_user1_id, 2)     

    standupactive1 = standup_active_v1(user1_token, channel_user1_id)
    assert standupactive1['is_active'] == True
    assert standupactive1['finishtime'] == standup_1['finishtime']

    standupactive2 = standup_active_v1(user1_token, channel_user2_id)
    assert standupactive2['is_active'] == False
    assert standupactive2['finishtime'] == None


def test_stand_send_invalidchannelid():
    #clear
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'du', 'asdf')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create a channel 
    channel_user1_id = channels_create_v2(user1_token,'gitb',True).get('channel_id')

    channel_item = channel_user1_id + 1
    with pytest.raises(InputError):
        standup_send_v1(user1_token, channel_item,'')

def test_stand_send_no_active():
    #clear
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'df', 'asdf')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create a channel 
    channel_user1_id = channels_create_v2(user1_token,'gitb',True).get('channel_id')

    with pytest.raises(InputError):
        standup_send_v1(user1_token, channel_user1_id,'')

def test_stand_send_not_member():
    clear_v2()

    #create and login in two users
    user1 = auth_register_v2('dbdqwe3@gmail.com', 'qwerasdf', 'df', 'asdf')
    user1 = auth_login_v2('dbdqwe3@gmail.com', 'qwerasdf')
    user1_token = user1['token']
    user2 = auth_register_v2('qweaqwed@gmail.com', 'tyuighjk', 'df2', 'asdf2')
    user2 = auth_login_v2('qweaqwed@gmail.com', 'tyuighjk')
    user2_token = user2['token']

    #create a channel 
    channel_user1_id = channels_create_v2(user1_token,'gitb',True).get('channel_id')

    with pytest.raises(AccessError):
        standup_send_v1(user2_token, channel_user1_id,'')

def test_standup_long_message():
    clear_v2()

    #create and login in user
    user1 = auth_register_v2('qwerasdf@gmail.com', 'qwerasdf', 'df', 'asdf')
    user1 = auth_login_v2('qwerasdf@gmail.com', 'qwerasdf')
    user1_token = user1['token']

    #create a channel 
    channel_user1_id = channels_create_v2(user1_token,'gitb',True).get('channel_id')

    #longmessage check
    message = "jjjjj"
    message = 2000 * message
    with pytest.raises(InputError):
        standup_send_v1(user1_token, channel_user1_id, message)