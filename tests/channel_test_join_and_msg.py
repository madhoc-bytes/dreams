'''Import pytest and relevant functions'''
import pytest

from src.auth import auth_register_v1
from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_join_channel():
    pass

def test_join_invalid_uid():
    pass

def test_join_invalid_channel_id():
    pass

def test_messages_nomessage():
    pass

def test_messages_invalid_uid():
    pass

def test_messages_invalid_ch_id():
    pass

def test_messages_start_too_big():
    pass

def test_messages_not_member():
    pass
