import streamlit as st
from google import genai
from gtts import gTTS

st.set_page_config(page_title="Assistant Manassé", page_icon="🇨🇩")
st.image("Logo.jpeg", width=200)
st.title("Assistant Manassé")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Mbote Manassé !"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        texte = response.text
        st.write(texte)
        tts = gTTS(text=texte[:400], lang='fr')
        tts.save("voix.mp3")
        st.audio("voix.mp3", autoplay=True)
        st.session_state.messages.append({"role": "assistant", "content": texte})
