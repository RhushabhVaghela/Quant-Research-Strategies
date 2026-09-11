from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import pytest

from src.data.kite_auth import update_env_file, save_access_token_file, ZerodhaAuthenticator

def test_update_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("KITE_API_KEY=test_key\nKITE_ACCESS_TOKEN=old_token\n")

    update_env_file("KITE_ACCESS_TOKEN", "new_token_123", env_path=env_file)
    content = env_file.read_text()

    assert "KITE_ACCESS_TOKEN=new_token_123" in content
    assert "KITE_API_KEY=test_key" in content

def test_save_access_token_file(tmp_path):
    token_file = tmp_path / "access_token.txt"
    save_access_token_file("test_token_abc", token_path=token_file)

    assert token_file.read_text() == "test_token_abc"

@patch("src.data.kite_auth.KiteConnect")
def test_is_token_valid_true(mock_kite_cls):
    mock_instance = MagicMock()
    mock_instance.profile.return_value = {"user_id": "IVN837", "user_name": "Rhushabh"}
    mock_kite_cls.return_value = mock_instance

    auth = ZerodhaAuthenticator(api_key="mock_key")
    assert auth.is_token_valid(access_token="mock_token") is True

@patch("src.data.kite_auth.KiteConnect")
def test_is_token_valid_false(mock_kite_cls):
    mock_instance = MagicMock()
    mock_instance.profile.side_effect = Exception("Token Exception")
    mock_kite_cls.return_value = mock_instance

    auth = ZerodhaAuthenticator(api_key="mock_key")
    assert auth.is_token_valid(access_token="invalid_token") is False
