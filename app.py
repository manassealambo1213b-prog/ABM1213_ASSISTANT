import os
import socket
import streamlit as st
from dotenv import load_dotenv

# 1. Chargement de l'environnement & Fix IPv4 Windows
load_dotenv()

old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

from google import genai
from google.genai import types

# 2. Importation des skills
from skills.system_skills import (
    list_files, git_status, create_file, read_file_content, get_system_time
)
from skills.app_skills import (
    add_task, list_tasks, complete_task, delete_task, get_weather
)

# Configuration de la page Streamlit
st.set_page_config(page_title="Mini Assistant IA", page_icon="🤖", layout="centered")
st.title("🤖 Mini Assistant IA")
st.caption("Assistant Gemini avec gestion de tâches et outils système")

def load_system_instruction():
    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            return f.read()
    return "Tu es un assistant IA."

# 3. Initialisation du client et du chat en session
if "chat" not in st.session_state:
    client = genai.Client()
    st.session_state.chat = client.chats.create(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=load_system_instruction(),
            tools=[
                list_files, git_status, create_file, 
                read_file_content, get_system_time,
                add_task, list_tasks, complete_task, 
                delete_task, get_weather
            ],
            temperature=0.2,
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Saisie utilisateur
if prompt := st.chat_input("Posez votre question à l'assistant..."):
    # Affichage du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erreur : {e}")