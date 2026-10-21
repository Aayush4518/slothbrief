
from unittest.mock import Mock, patch

import pytest
import requests

from src.slothbrief.ollama_client import (
    DEFAULT_MODEL,
    OLLAMA_URL,
    OllamaError,
    generate_response,
)


@patch("src.slothbrief.ollama_client.requests.post")
def test_generate_response_success(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "A concise summary"}
    mock_post.return_value = mock_response

    result = generate_response("Summarize this text")

    assert result == "A concise summary"
    mock_post.assert_called_once_with(
        OLLAMA_URL,
        json={
            "model": DEFAULT_MODEL,
            "prompt": "Summarize this text",
            "stream": False,
        },
        timeout=180,
    )


@patch("src.slothbrief.ollama_client.requests.post")
def test_generate_response_empty_result(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "   "}
    mock_post.return_value = mock_response

    with pytest.raises(OllamaError, match="empty response"):
        generate_response("Some text")


@patch("src.slothbrief.ollama_client.requests.post")
def test_generate_response_connection_error(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError()

    with pytest.raises(OllamaError, match="Cannot connect to Ollama"):
        generate_response("Some text")


@patch("src.slothbrief.ollama_client.requests.post")
def test_generate_response_timeout(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout()

    with pytest.raises(OllamaError, match="too long to respond"):
        generate_response("Some text")


@patch("src.slothbrief.ollama_client.requests.post")
def test_generate_response_missing_model(mock_post):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response

    with pytest.raises(OllamaError, match="ollama pull"):
        generate_response("Some text", model="missing-model")
