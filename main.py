import os
import socket
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# 1. Chargement des variables d'environnement (.env)
load_dotenv()

# 2. Résolution IPv4 pour éviter les erreurs DNS sous Windows
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

# 3. Importation des fonctions (skills)
from skills.system_skills import (
    list_files, 
    git_status, 
    create_file, 
    read_file_content, 
    get_system_time
)
from skills.app_skills import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    get_weather
)

def load_system_instruction():
    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            return f.read()
    return "Tu es un assistant IA."

# 4. Initialisation du client avec le bon modèle gemini-3.8-flash
client = genai.Client()

chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction=load_system_instruction(),
        tools=[
            list_files, 
            git_status, 
            create_file, 
            read_file_content, 
            get_system_time,
            add_task,
            list_tasks,
            complete_task,
            delete_task,
            get_weather
        ],
        temperature=0.2,
    )
)

print("🤖 Assistant prêt ! Tapez 'exit' pour quitter.\n")

# 5. Boucle principale
while True:
    user_input = input("Vous : ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    try:
        response = chat.send_message(user_input)
        print(f"\nAssistant : {response.text}\n")
    except ServerError:
        print("\n⚠️ Le serveur Gemini subit un fort trafic. Réessayez dans quelques secondes...\n")
    except Exception as e:
        print(f"\nErreur : {e}\n")