import pytest
from src.data import channels, users, dms
from src.message import message_sendlater_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from datetime import datetime, timezone, timedelta
from threading import Timer
import time

def test_message_sendlater_basic():
    clear_v2()
    #create a user and channel
    auth_token = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')['token']
    test_channel = channels_create_v2(auth_token, "test channel", True)['channel_id']
    channel_join_v2(auth_token, test_channel)

    #make a time sent
    time_sent = int((datetime.utcnow() + timedelta(seconds=1)).replace(tzinfo=timezone.utc).timestamp())
    message_sendlater_v1(auth_token, test_channel, "message", time_sent)
    time.sleep(1)
    test_message = channel_messages_v2(auth_token, test_channel , 0)['messages']
    ### FIX
    assert test_message[message_string] == "message"