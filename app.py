
import streamlit as st

from src.slothbrief.ollama_client import OllamaError
from src.slothbrief.summarizer import summarize_text
from src.slothbrief.file_reader import read_uploaded_file

st.set_page_config(
    page_title="SlothBrief",
    page_icon="🦥",
    layout="centered",
)

if "summary" not in st.session_state:
    st.session_state.summary = ""

st.title("🦥 SlothBrief")
st.caption("Slow down. Understand more. Your text stays local.")

st.write(
    "Turn meeting notes, long messages, and chat logs into "
    "concise summaries using your local AI model."
)


uploaded_file = st.file_uploader(
    "Upload a text file (optional)",
    type=["txt", "md"],
    help="Upload a .txt or .md file, or paste your text below.",
)

pasted_text = st.text_area(
    "Or paste your text",
    height=260,
    placeholder="Paste your meeting notes or chat log here...",
)

if uploaded_file is not None:
    try:
        file_text = read_uploaded_file(uploaded_file)
    except ValueError as error:
        st.error(str(error))
        file_text = ""
else:
    file_text = ""

text = file_text if uploaded_file is not None else pasted_text


summary_length = st.selectbox(
    "Summary length",
    options=["short", "balanced", "detailed"],
    index=1,
    format_func=lambda value: value.capitalize(),
)




if st.button("Generate Summary", type="primary", use_container_width=True):
    if not text or not text.strip():
        st.warning("Please paste some text or upload a text file first.")
    else:
        try:
            with st.spinner("SlothBrief is thinking locally..."):
                st.session_state.summary = summarize_text(
                    text,
                    length=summary_length,
                )
        except OllamaError as error:
            st.error(str(error))
        except ValueError as error:
            st.warning(str(error))


if st.session_state.summary:
    st.divider()
    st.subheader("Your Results")
    st.markdown(st.session_state.summary)

    st.download_button(
        label="Download as Markdown",
        data=st.session_state.summary,
        file_name="slothbrief-summary.md",
        mime="text/markdown",
        use_container_width=True,
    )
