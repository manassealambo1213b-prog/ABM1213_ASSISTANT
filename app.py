import streamlit as st
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from skills.system_skills import list_files, git_status, create_file, read_file_content, get_system_time
from skills.app_skills import add_task, list_tasks, complete_task, delete_task, get_weather

load_dotenv()

def load_system_instruction():
    try:
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Tu es un assistant utile."

st.set_page_config(page_title="Mini Assistant", page_icon="🤖")
st.title("🤖 Mini assistant")

client = genai.Client()

# Modèles valides en octobre 2026 d'après Google
MODELES = [
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
]

def get_chat(model_name=None):
    liste = [model_name] if model_name else MODELES
    for nom in liste:
        try:
            chat = client.chats.create(
                model=nom,
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
            return chat, nom
        except Exception as e:
            print(f"❌ {nom}: {e}")
            continue
    return None, None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state or "model_name" not in st.session_state:
    chat, model_used = get_chat()
    if chat is None:
        st.error("Tous les modèles sont indisponibles. Réessaie dans 1 minute.")
        st.stop()
    st.session_state.chat = chat
    st.session_state.model_name = model_used

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question à l'assistant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Connecté sur {st.session_state.model_name}..."):
            response_text = None
            last_error = ""
            for essai_model in MODELES:
                try:
                    if essai_model != st.session_state.model_name:
                        chat, _ = get_chat(essai_model)
                        if chat:
                            st.session_state.chat = chat
                            st.session_state.model_name = essai_model
                    
                    response = st.session_state.chat.send_message(prompt)
                    response_text = response.text
                    break
                except Exception as e:
                    last_error = str(e)
                    # On retry pour 503, 404, client closed
                    if any(x in last_error for x in ["503", "404", "UNAVAILABLE", "NOT_FOUND", "client has been closed"]):
                        print(f"Retry {essai_model} -> {last_error[:100]}")
                        time.sleep(1)
                        continue
                    else:
                        break
            
            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error(f"Erreur finale: {last_error}")