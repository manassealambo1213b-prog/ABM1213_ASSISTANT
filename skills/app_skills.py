import json
import os
import urllib.request
import urllib.parse

TASKS_FILE = "tasks.json"

# --- MODULE GESTIONNAIRE DE TÂCHES ---

def _load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def add_task(title: str) -> str:
    """Ajoute une nouvelle tâche à la liste de tâches."""
    tasks = _load_tasks()
    task = {"id": len(tasks) + 1, "title": title, "completed": False}
    tasks.append(task)
    _save_tasks(tasks)
    return f"Tâche '{title}' ajoutée avec succès !"

def list_tasks() -> str:
    """Affiche la liste de toutes les tâches enregistrées."""
    tasks = _load_tasks()
    if not tasks:
        return "Aucune tâche enregistrée."
    
    result = []
    for task in tasks:
        status = "✔" if task["completed"] else "❌"
        result.append(f"[{status}] {task['id']}. {task['title']}")
    return "\n".join(result)

def complete_task(task_id: int) -> str:
    """Marque une tâche comme terminée en utilisant son ID."""
    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            _save_tasks(tasks)
            return f"Tâche {task_id} marquée comme terminée !"
    return f"Tâche {task_id} introuvable."

def delete_task(task_id: int) -> str:
    """Supprime une tâche à partir de son ID."""
    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            # Réindexation des identifiants
            for index, t in enumerate(tasks, start=1):
                t["id"] = index
            _save_tasks(tasks)
            return f"Tâche {task_id} supprimée."
    return f"Tâche {task_id} introuvable."


# --- MODULE MÉTÉO ---

def get_weather(city: str) -> str:
    """Récupère la météo actuelle pour une ville donnée."""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['lang_fr'][0]['value'] if 'lang_fr' in current else current['weatherDesc'][0]['value']
            return f"À {city.capitalize()}, il fait actuellement {temp_c}°C avec {desc}."
    except Exception as e:
        return f"Impossible de récupérer la météo pour '{city}' ({str(e)})."