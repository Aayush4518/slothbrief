# How SlothBrief Works

SlothBrief takes a block of text and turns it into a summary, key points, and action items. It uses a local Ollama model, so there's no need for a paid AI API.

## Project Structure

- `app.py` - The Streamlit interface. Users paste text here, generate a summary, and download the result.
- `src/slothbrief/summarizer.py` - Checks the input and builds the prompt sent to the model.
- `src/slothbrief/ollama_client.py` - Sends requests to Ollama and handles errors.
- `tests/` - Tests for the summarizer and Ollama client.
- `samples/` - Sample text to try in the app.

## What Happens When You Summarize

1. You paste some text into the app.
2. The summarizer checks that the input isn't empty.
3. The prompt is sent to Ollama, which runs the model locally.
4. The result appears in the app, where you can download it as a Markdown file.

## Running Tests

The tests use mocked responses, so they don't need to run the AI model.

```powershell
python -m pytest -v
```

## Privacy

SlothBrief sends text to the Ollama service running on your machine for summarization. It doesn't use a cloud AI API.