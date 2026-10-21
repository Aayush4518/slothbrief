
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:1.5b"


class OllamaError(Exception):
    """Raised when Ollama cannot generate a response."""


def generate_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
    timeout: int = 180,
) -> str:
    """Generate text using a locally running Ollama model."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=timeout,
        )

        if response.status_code == 404:
            raise OllamaError(
                f"Model '{model}' may not be installed. "
                f"Run: ollama pull {model}"
            )

        response.raise_for_status()
        result = response.json().get("response", "").strip()

        if not result:
            raise OllamaError("Ollama returned an empty response.")

        return result

    except OllamaError:
        raise

    except requests.exceptions.ConnectionError as exc:
        raise OllamaError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise OllamaError(
            "Ollama took too long to respond. Try shorter text."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        raise OllamaError(f"Ollama returned an HTTP error: {exc}") from exc

    except requests.exceptions.RequestException as exc:
        raise OllamaError(
            f"Could not communicate with Ollama: {exc}"
        ) from exc

    except ValueError as exc:
        raise OllamaError(
            "Ollama returned an invalid response."
        ) from exc
