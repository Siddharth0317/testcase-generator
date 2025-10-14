import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

API_URL = ("api_url", "http://localhost:8000")

# --- Page setup ---
st.set_page_config(page_title="Test Case Generator", page_icon="🧠", layout="wide")

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        color: #4E9F3D;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 2rem;
    }
    .test-box {
        background-color: #F7F9FB;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.markdown('<div class="main-title">🧠 AI-powered Test Case Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate software test cases instantly from plain-text requirements</div>', unsafe_allow_html=True)

add_vertical_space(1)

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

if st.button("🚀 Generate Test Cases", use_container_width=True):
    if not req.strip():
        st.warning("Please enter a valid requirement first.")
    else:
        with st.spinner("Analyzing and generating test cases..."):
            resp = requests.post(f"{API_URL}/generate", json={"requirement": req})
            if resp.status_code == 200:
                tests = resp.json()
                st.success(f"✅ Generated {len(tests)} test case(s).")
                for t in tests:
                    with st.container():
                        st.markdown('<div class="test-box">', unsafe_allow_html=True)
                        st.subheader(t["title"])
                        st.caption(f"Type: {t['type'].capitalize()}")
                        st.markdown(f"**Description:** {t['description']}")
                        st.markdown("**Steps:**")
                        for s in t["steps"]:
                            st.write(f"• {s}")
                        st.markdown(f"**Expected Outcome:** {t['expected']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        add_vertical_space(1)
            else:
                st.error(f"API error: {resp.text}")

st.markdown("---")
st.caption("Developed with ❤️ using FastAPI, spaCy, and Streamlit.")