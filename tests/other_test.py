from other import clear_v1, data_channels, data_user

def test_clear_v1():
    clear_v1()
    assert data_channels() == 0
    assert data_user() == 0