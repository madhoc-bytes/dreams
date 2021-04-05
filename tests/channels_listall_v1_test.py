# Test file for channels_listall_v1

# Imports
import pytest
from src.auth import auth_register_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.error import InputError, AccessError

# Test for a list with no channels details in it
def test_no_channels_listall():
    pass

# Test for a list with a unique channel 
def test_unique_channels_listall():
    pass


# Test for a list with exactly two channels in it
def test_double_channels_listall():
    pass


# Test where there are 3 channels, in which the user has access to 1
def test_channels_with_user_access():
    pass