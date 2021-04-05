import pytest
import requests
import json
from src import config

def test_basic():
    payload = requests.get(config.url + 'channel', params={'data': 'hello'})