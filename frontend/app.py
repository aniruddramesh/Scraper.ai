import streamlit as st
import requests

st.set_page_config(page_title="Scraper.ai", page_icon="🕸️", layout="centered")

st.title("Scraper.ai - Dig and Dust")
st.write("Enter a URL and an AI prompt. The backend will scrape the page and format it according to the prompt.")

backend_default = "http://127.0.0.1:5000/process"
# backend_url = st.text_input("Backend endpoint", value=backend_default)

# User inputs
url = st.text_input("Website URL", placeholder="https://example.com/...")
prompt = st.text_area("AI Prompt (instructions for formatting/extraction)", height=150,
                      value="Summarize the page in 5 bullet points.")
prefer_selenium = st.checkbox("Prefer Selenium (use browser scraping; slower but handles JS)", value=True)

col1, col2 = st.columns([1, 1])
with col1:
    submit = st.button("Scrape & Process")
with col2:
    clear = st.button("Clear")

# Clear action
if clear:
    st.rerun()

# When user submits
if submit:
    if not url.strip():
        st.error("Please enter a website URL.")
    elif not prompt.strip():
        st.error("Please enter an AI prompt.")
    else:
        payload = {
            "url": url.strip(),
            "prompt": prompt.strip(),
            "prefer_selenium": bool(prefer_selenium)
        }

        try:
            with st.spinner("Contacting backend and processing... (this can take a few seconds)"):
                resp = requests.post(backend_default, json=payload, timeout=120)

            # Handle non-200 responses
            if resp.status_code != 200:
                # Try to show JSON error, otherwise raw text
                try:
                    err = resp.json()
                    st.error(f"Error: {err}")
                except Exception:
                    st.error(f"Server returned status {resp.status_code}: {resp.text}")
            else:
                data = resp.json()

                # Common field names fallback
                result = data.get("result") or data.get("response") or data.get("ai_output") or None

                st.subheader("AI Result")
                if result:
                    # Display as markdown for nicer formatting
                    st.markdown(result)
                    st.download_button("Download result (.txt)", result, file_name="scraped_result.txt")
                else:
                    st.info("No `result` field in response — showing full JSON response below.")
                    st.json(data)

                # If backend returns scraped snippet, show it (collapsed)
                raw_snippet = data.get("raw_text_snippet") or data.get("scraped_text") or data.get("raw")
                if raw_snippet:
                    with st.expander("Show raw scraped text (first 20k chars)"):
                        st.code(raw_snippet[:20000], language="text")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
