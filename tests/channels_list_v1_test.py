# Test file for channels_list_v1

# Imports
import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.error import InputError, AccessError


# Test for a list without any channel details in it
def test_no_channels_in_list():
    pass


# Test for a list with only one channel details in it
def test_one_channel_in_list():
    pass

# Test for a list with exactly two channels in it
def test_two_channels_in_list():
    pass


# Test where user is authorized to access 1 channel, when there are 2 channels in total
def test_two_users_channels_list():
    pass

# Test where user is part of no channels, and there are 2 different channels available
def test_two_users_not_in_channels():
    pass