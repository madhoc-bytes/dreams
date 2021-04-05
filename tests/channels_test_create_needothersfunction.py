import pytest

from src.channels import channels_create_v2 
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v2

# test if channels can be created correctly
def test_channels_create_v2():
    clear_v2()
    c1 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    assert channels_create_v2(c1['token'], 'first', True) == {'id' : 0}
    assert channels_create_v2(c1['token'], 'second', False) == {'id' : 1}

# test the error stituation
def tests_channels_create_v2_except():
    clear_v2()
    auth_user_id11 = auth_register_v1("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    with pytest.raises(InputError):
        channels_create_v2(auth_user_id11['token'], "kasbfvkabvadfihviadfvbhidfbuiva", False)
