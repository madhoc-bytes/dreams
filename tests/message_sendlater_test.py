import pytest
from src.data import channels, users, dms
from src.message import message_sendlater_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from datetime import datetime, timezone, timedelta
from src.error import AccessError, InputError
from threading import Timer
import time

def test_message_sendlater_notinch():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    second_token = auth_register_v2('test_second@gmail.com', 'test_pw_second', 'testfs', 'testls')['token']
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    channel_join_v2(second_token, test_channel)
    with pytest.raises(AccessError):
        message_sendlater_v1(auth_token, test_channel, 'message', time_sent)

def test_message_sendlater_basic():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    # Get the current time and add a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    message_sendlater_v1(auth_token, test_channel, "message", time_sent)
    time.sleep(1)
    test_message = channel_messages_v2(auth_token, test_channel , 0)['messages']

    assert test_message[0]['message'] == "message"

def test_message_sendlater_timeinpast():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    # Get the current time and minus a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) - 1
    with pytest.raises(InputError):
        message_sendlater_v1(auth_token, test_channel, "message", time_sent)

def test_message_sendlater_invalid_ch():
    clear_v2()

    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    with pytest.raises(InputError):
        message_sendlater_v1(auth_token, 'invalid', "message", time_sent)

def test_message_sendlater_exceed_character_limit():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    # Get the current time and add a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    long_string = "asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa"
    with pytest.raises(InputError):
        message_sendlater_v1(auth_token, test_channel, long_string, time_sent)

