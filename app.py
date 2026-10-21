
import streamlit as st

from src.slothbrief.ollama_client import OllamaError
from src.slothbrief.summarizer import summarize_text

st.set_page_config(
    page_title="SlothBrief",
    page_icon="🦥",
    layout="centered",
)

st.title("🦥 SlothBrief")
st.caption("Slow down. Understand more. Your text stays local.")

st.write(
    "Turn meeting notes, long messages, and chat logs into "
    "concise summaries using your local AI model."
)

text = st.text_area(
    "Paste your text",
    height=260,
    placeholder="Paste your meeting notes or chat log here...",
)

if "summary" not in st.session_state:
    st.session_state.summary = ""

if st.button("Generate Summary", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        try:
            with st.spinner("SlothBrief is thinking locally..."):
                st.session_state.summary = summarize_text(text)
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
