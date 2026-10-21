
# How SlothBrief Works

SlothBrief uses Streamlit for the interface and Ollama to run the language model locally.

## Files

- `app.py` handles text input, file uploads, summary options, and downloads.
- `src/slothbrief/file_reader.py` reads uploaded UTF-8 text and Markdown files.
- `src/slothbrief/summarizer.py` validates input and builds the summary prompt.
- `src/slothbrief/ollama_client.py` sends requests to Ollama and handles errors.
- `tests/` contains the automated tests.

## Flow

1. The user pastes text or uploads a file.
2. SlothBrief reads and validates the input.
3. The user chooses a summary length.
4. The prompt is sent to the local Ollama model.
5. The result appears in the app and can be downloaded as Markdown.

## Testing

Run `python -m pytest -v`. The unit tests mock HTTP requests, so they don't need a running model.
