import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="BuildGuide UK", 
    page_icon="🛠️", 
    layout="centered"
)

# Professional styling
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom, #f8fafc, #e2e8f0); }
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e40af);
        padding: 50px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 40px;
        color: white;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
    }
    .title { font-size: 56px; font-weight: 700; margin: 0; letter-spacing: -2px; }
    .subtitle { font-size: 25px; margin: 12px 0 0 0; opacity: 0.95; }
    .description { max-width: 720px; margin: 25px auto 0; font-size: 18px; line-height: 1.6; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="title">BuildGuide UK</h1>
    <p class="subtitle">Construction Guidance to UK Regulation Standards</p>
    <p class="description">
        Your practical on-site assistant for detailed method statements, 
        risk assessments, step-by-step instructions and compliant building advice.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    st.success("✅ Groq Connected")
    st.caption("Version 1.7")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

SYSTEM_PROMPT = """
You are BuildGuide UK, an experienced UK construction foreman with 20+ years on site.
When the user asks how to do any construction task, ALWAYS structure your answer like this:

1. **Method Statement**
   - Very detailed, practical, numbered step-by-step instructions from ground up
   - Real-world tips that a tradesperson would actually use on site
   - Reference relevant UK Building Regulations and NHBC Standards

2. **Risk Assessment**
   - Main hazards
   - Who might be harmed
   - Control measures
   - PPE required
   - Common mistakes to avoid

3. **Materials Needed**
   - Realistic quantities for a typical job
   - Local supplier suggestions (Jewson, Travis Perkins, Selco, etc.)

Be practical and detailed. Always end with the disclaimer.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g. How do I build foundations for a small extension from ground up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # This line uses Streamlit Secrets (recommended for cloud deployment)
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2200,
                stream=True,
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)[:200]}")

        st.session_state.messages.append({"role": "assistant", "content": full_response})

st.caption("Made for UK builders • Always verify with professionals and building control")