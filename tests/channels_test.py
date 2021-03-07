import pytest
from src.channel import channel_join_v1
from src.channels import channels_create_v1 
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

# test if channels can be created correctly
def test_channels_create_v1():
    clear_v1()
    auth_user_id00 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    assert channels_create_v1(auth_user_id00, 'first', True) == {'id' : 0}
    assert channels_create_v1(auth_user_id00, 'second', False) == {'id' : 1}

# test the error stituation
def tests_channels_create_v1_except():
    clear_v1()
    auth_user_id11 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id11, "kasbfvkabvadfihviadfvbhidfbuiva", False)

def test_channels_list_v1():
    clear_v1()
    auth_user_id00 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    auth_user_id01 = auth_register_v1("dubwe28945@gmail.com", "xujdwen", "Leo", "Fitz")
    channels_create_v1(auth_user_id00, 'first', True)
    channels_create_v1(auth_user_id00, 'second', True)
    channels_create_v1(auth_user_id00, 'third', True)
    channel_join_v1(auth_user_id01, 0)
    channel_join_v1(auth_user_id01, 2)
    assert channels_list_v1(auth_user_id01)['channels'] == \
    [{'id': 0, 'name': 'first'},
     {'id': 2, 'name': 'third'}]








