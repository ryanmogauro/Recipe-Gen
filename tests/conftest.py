# tests/conftest.py
import sys
import os
import pytest
from unittest.mock import MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as c:
        yield c

@pytest.fixture
def mock_openai(mocker):
    """
    Mocks website.views.OpenAI to handle three scenarios:
    1) "macaroni" + "cheese" => "Here’s your mac & cheese recipe!"
    2) "anything" => content=None => "Sorry, I don’t understand that."
    3) everything else => "Some other generic recipe."
    """
    mock_class = mocker.patch("website.views.OpenAI")

    def fake_create(model, messages):
        user_content = messages[0].get("content", "").lower()

        if "macaroni" in user_content and "cheese" in user_content:
            content = "Here’s your mac & cheese recipe!"
        elif "anything" in user_content:
            # Force content=None => triggers "Sorry, I don't understand that."
            content = None
        else:
            content = "Some other generic recipe."

        fake_completion = MagicMock()
        fake_completion.choices = [
            MagicMock(message=MagicMock(content=content))
        ]
        return fake_completion

    mock_chat = MagicMock()
    mock_chat.completions.create.side_effect = fake_create

    mock_instance = MagicMock()
    mock_instance.chat = mock_chat

    mock_class.return_value = mock_instance
    return mock_class
