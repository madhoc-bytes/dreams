import pytest
import src.channels
import src.auth
from src.error import InputError, AccessError
from src.other import clear_v1

# test if channels can be created correctly
def test_channels_create_v1():
    clear_v1()
    auth_user_id00 = auth.auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    assert channels.channels_create_v1(auth_user_id00, 'first', True) == {'channel_id' : 0}
    assert channels.channels_create_v1(auth_user_id00, 'second', False) == {'channel_id' : 1}

# test the error stituation
def tests_channels_create_v1_except():
    clear_v1()
    auth_user_id11 = auth.auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    with pytest.raises(AccessError):
        channels.channels_create_v1(auth_user_id11, 'sadskfjh', True)
    with pytest.raises(InputError):
        channels.channels_create_v1(auth_user_id11, "kasbfvkabvadfihviadfvbhidfbuiva", False)
