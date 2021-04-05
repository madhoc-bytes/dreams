from src.other import clear_v2, data_channels, data_user
import pytest

def test_clear_v2():
    clear_v2()
    assert data_channels() == 0
    assert data_user() == 0
