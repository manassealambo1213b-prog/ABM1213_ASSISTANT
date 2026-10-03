import os
import subprocess
from datetime import datetime

# --- Outils système ---

def list_files(path: str = ".") -> str:
    """Renvoyer la liste des fichiers dans le dossier spécifié.
    
    Args:
        path: Le chemin du dossier à lister (par défaut le dossier courant '.').
    """
    try:
        files = os.listdir(path)
        return f"Fichiers dans '{path}': {', '.join(files)}"
    except Exception as e:
        return f"Erreur lors de la lecture du dossier : {e}"

def git_status() -> str:
    """Renvoyer le résultat de la commande 'git status'."""
    try:
        result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            return output if output else "Le dépôt Git est propre."
        return "Ce dossier n'est pas un dépôt Git."
    except Exception as e:
        return f"Erreur lors de l'exécution de git status : {e}"

def create_file(filename: str, content: str) -> str:
    """Créer un nouveau fichier texte avec du contenu spécifié.
    
    Args:
        filename: Le nom du fichier à créer (ex: 'notes.txt' ou 'test.py').
        content: Le texte ou le code à écrire à l'intérieur du fichier.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Le fichier '{filename}' a été créé avec succès."
    except Exception as e:
        return f"Erreur lors de la création du fichier : {e}"

def read_file_content(filename: str) -> str:
    """Lire et renvoyer le contenu textuel d'un fichier.
    
    Args:
        filename: Le nom ou le chemin du fichier à lire.
    """
    try:
        if not os.path.exists(filename):
            return f"Erreur : Le fichier '{filename}' n'existe pas."
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erreur lors de la lecture du fichier : {e}"

def get_system_time() -> str:
    """Renvoyer la date et l'heure actuelles du système."""
    now = datetime.now()
    return now.strftime("Nous sommes le %d/%m/%Y et il est %H:%M:%S.")