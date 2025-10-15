import streamlit as st
import requests
import pandas as pd
import json
from streamlit_extras.add_vertical_space import add_vertical_space

API_URL = "http://localhost:8000"

# --- Page Setup ---
st.set_page_config(page_title="AI Test Case Generator", page_icon="🧠", layout="wide")

# --- Custom CSS for aesthetics ---
st.markdown("""
<style>
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    color: #1E3D59;
    margin-bottom: 0.3rem;
}
.subtitle {
    font-size: 1.2rem;
    text-align: center;
    color: #4E9F3D;
    margin-bottom: 2rem;
}
.test-box {
    background: linear-gradient(135deg, #F9F9F9 0%, #E0F7FA 100%);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
.test-box h3 {
    color: #1E3D59;
}
.export-btn {
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="main-title">🧠 AI-powered Test Case Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate software test cases instantly from plain-text requirements</div>', unsafe_allow_html=True)

add_vertical_space(1)

# --- Input Section ---
col1, col2 = st.columns([2,1])
with col1:
    req = st.text_area(
        "Enter your requirement or user story:",
        height=150,
        placeholder="Example: The system should allow users to upload images up to 5MB"
    )
with col2:
    st.info("💡 Tip: Write one clear requirement at a time for best results.")

add_vertical_space(1)

generated_tests = []

# --- Generate Test Cases ---
if st.button("🚀 Generate Test Cases", use_container_width=True):
    if not req.strip():
        st.warning("Please enter a valid requirement first.")
    else:
        with st.spinner("Analyzing and generating test cases..."):
            try:
                resp = requests.post(f"{API_URL}/generate", json={"requirement": req})
                resp.raise_for_status()
                generated_tests = resp.json()
                st.success(f"✅ Generated {len(generated_tests)} test case(s).")
            except Exception as e:
                st.error(f"API error: {e}")

# --- Display Test Cases ---
for t in generated_tests:
    with st.container():
        st.markdown('<div class="test-box">', unsafe_allow_html=True)
        st.subheader(f"📝 {t['title']}")
        st.caption(f"Category: {t['type'].capitalize()}")
        st.markdown(f"**Description:** {t['description']}")
        st.markdown("**Steps:**")
        for s in t["steps"]:
            st.markdown(f"- {s}")
        st.markdown(f"**Expected Outcome:** {t['expected']}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Export Buttons ---
if generated_tests:
    st.markdown("---")
    st.subheader("Export Test Cases")
    export_col1, export_col2, export_col3 = st.columns(3)

    # CSV Export
    with export_col1:
        csv_df = pd.DataFrame(generated_tests)
        csv_df['steps'] = csv_df['steps'].apply(lambda x: "\n".join(x))
        csv_data = csv_df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 CSV", csv_data, "test_cases.csv", "text/csv")

    # PDF Export
    with export_col2:
        try:
            pdf_resp = requests.post(f"{API_URL}/export/pdf", json=generated_tests)
            if pdf_resp.status_code == 200:
                st.download_button("📄 PDF", pdf_resp.content, "test_cases.pdf", "application/pdf")
        except:
            st.warning("PDF export failed")

    if generated_tests:
        try:
            resp = requests.post(
                f"{API_URL}/generate_selenium",
                json=generated_tests,
                headers={"Content-Type": "application/json"}
            )
            if resp.status_code == 200:
                st.download_button(
                    label="🤖 Selenium Script",
                    data=resp.content,
                    file_name="selenium_test_cases.py",
                    mime="text/x-python"
                )
            else:
                st.error(f"Selenium export failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Selenium export failed: {e}")
