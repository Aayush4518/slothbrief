
def read_uploaded_file(uploaded_file) -> str:
    """Read an uploaded UTF-8 text or Markdown file."""

    try:
        return uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "This file isn't valid UTF-8 text. "
            "Please save it as UTF-8 and try again."
        ) from exc
