import pytest
from src.auth import auth_register_v2
from src.dm_create_v2 import dm_create_v2
from src.error import InputError, AccessError
from src.other import clear_v2
from src.message_senddm_v2 import message_senddm_v2

def test_long_1000_dm_messsages():
    clear_v2()
    information1 = auth_register_v2("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    dm_id1 = dm_create_v2(information1['token'], 'long_1000_dm_messsages', True)
    with pytest.raises(InputError):
        assert message_senddm_v2(information1['token'], dm_id1['dm_id'],'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

def not_owner_send_dm_message():
    clear_v2()
    information1 = auth_register_v2("dubaida28951345@gmail.com", "xujiawen", "Jemma", "Simmons")
    dm_id1 = dm_create_v2(information1['token'], 'long_1000_dm_messsages', True)
    information2 = auth_register_v2("sdfgggh@gmail.com", "sdfgh", "wer", "ghshh")
    with pytest.raises(AccessError):
        assert message_senddm_v2(information2['token'], dm_id1['dm_id'], 'See')