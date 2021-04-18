import pytest
from src.data import channels, users, dms
from src.message import message_sendlaterdm_v1
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.channels import channels_create_v2
from src.other import clear_v2
from datetime import datetime, timezone, timedelta
from src.error import AccessError, InputError
from threading import Timer
import time

def test_message_sendlaterdm_basic():
    clear_v2()
    #create a user and dm
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    dm_id = dm_create_v1(auth_token,[])['dm_id']
    # Get the current time and add a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    message_sendlaterdm_v1(auth_token, dm_id, "message", time_sent)
    time.sleep(3)
    test_message = dm_messages_v1(auth_token, dm_id , 0)['messages']
    print(test_message)
    assert test_message[dm_id]['message'] == "message"

def test_message_sendlaterdm_timeinpast():
    clear_v2()
    #create a user and dm
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    dm_id = dm_create_v1(auth_token,[])['dm_id']

    # Get the current time and minus a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) - 1
    with pytest.raises(InputError):
        message_sendlaterdm_v1(auth_token, dm_id, "message", time_sent)

def test_message_sendlaterdm_invalid_dmid():
    clear_v2()

    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    with pytest.raises(InputError):
        message_sendlaterdm_v1(auth_token, 'invalid', "message", time_sent)

def test_message_sendlaterdm_exceed_character_limit():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    dm_id = dm_create_v1(auth_token,[])['dm_id']

    # Get the current time and add a second
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    long_string = "asdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaasdasdasdaa"
    with pytest.raises(InputError):
        message_sendlaterdm_v1(auth_token, dm_id, long_string, time_sent)

def test_message_sendlaterdm_notinch():
    clear_v2()

    #owner of dm/caller of dm_create
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    dm_id = dm_create_v1(auth_token,[])['dm_id']
    second_token = auth_register_v2('test_second@gmail.com', 'test_pw_second', 'testfs', 'testls')['token']
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 1
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(second_token, dm_id, 'message', time_sent)