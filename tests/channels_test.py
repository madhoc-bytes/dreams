import pytest

from src.channels import channels_create_v1 
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1

# test if channels can be created correctly
def test_channels_create_v1():
    clear_v1()
    auth_user_id00 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    assert channels_create_v1(auth_user_id00, 'first', True) == {'channel_id' : 0}
    assert channels_create_v1(auth_user_id00, 'second', False) == {'channel_id' : 1}

# test the error stituation
def tests_channels_create_v1_except():
    clear_v1()
    auth_user_id11 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    with pytest.raises(InputError):
        channels_create_v1(auth_user_id11, "kasbfvkabvadfihviadfvbhidfbuiva", False)
