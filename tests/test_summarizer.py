
from unittest.mock import patch

import pytest

from src.slothbrief.summarizer import summarize_text
from unittest.mock import Mock

from src.slothbrief.file_reader import read_uploaded_file


def test_summarize_valid_text():
    sample_text = "The team meeting is scheduled for Monday."
    expected_summary = "The team meeting is on Monday."

    with patch(
        "src.slothbrief.summarizer.generate_response",
        return_value=expected_summary,
    ) as mock_generate:
        result = summarize_text(sample_text)

    assert result == expected_summary
    mock_generate.assert_called_once()

    prompt = mock_generate.call_args.args[0]
    assert sample_text in prompt


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_summarize_empty_text(text):
    with patch(
        "src.slothbrief.summarizer.generate_response"
    ) as mock_generate:
        with pytest.raises(ValueError, match="Please provide text"):
            summarize_text(text)

    mock_generate.assert_not_called()






def test_read_uploaded_text_file():
    uploaded_file = Mock()
    uploaded_file.getvalue.return_value = b"Meeting notes for Monday."

    result = read_uploaded_file(uploaded_file)

    assert result == "Meeting notes for Monday."


def test_read_uploaded_markdown_file():
    uploaded_file = Mock()
    uploaded_file.getvalue.return_value = b"# Meeting Notes\n\n- Finish testing"

    result = read_uploaded_file(uploaded_file)

    assert result == "# Meeting Notes\n\n- Finish testing"


def test_read_uploaded_file_rejects_invalid_utf8():
    uploaded_file = Mock()
    uploaded_file.getvalue.return_value = b"\xff\xfe\xfa"

    import pytest

    with pytest.raises(ValueError, match="valid UTF-8"):
        read_uploaded_file(uploaded_file)
