import subprocess
import re
import sys

# Format attendu pour un TODO lié à une issue : TODO (#123)
TODO_PATTERN = re.compile(r"TODO\s+\(#(\d+)\)")

# Extensions de fichiers dans lesquels chercher les TODOs
FILES_TO_SCAN = ["--include=*.rs", "--include=*.py"]

# État d'une issue fermée sur GitHub
ISSUE_CLOSED = "CLOSED"


def find_todos():
    # Cherche récursivement tous les TODOs dans les fichiers Rust et Python
    # -r : récursif, -n : affiche le numéro de ligne
    # Retourne une liste de chaînes de la forme "fichier:ligne:contenu"
    result = subprocess.run(
        ["grep", "-rn", "TODO"] + FILES_TO_SCAN + ["."],
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def get_issue_state(issue_num):
    # Interroge l'API GitHub pour récupérer l'état de l'issue
    # Retourne "OPEN", "CLOSED", ou une chaîne vide si l'issue n'existe pas
    result = subprocess.run(
        ["gh", "issue", "view", issue_num, "--json", "state", "--jq", ".state"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def error(file_path, line_num, message):
    # Affiche une annotation d'erreur sur la ligne dans GitHub et dans les logs
    print(f"::error file={file_path},line={line_num}::{file_path}:{line_num} - {message}") - {message}")


def check_todo(file_path, line_num, content):
    # Vérifie qu'un TODO respecte le format attendu et référence une issue valide
    match = TODO_PATTERN.search(content)

    if not match:
        error(file_path, line_num, "TODO sans issue associée. Format attendu : TODO (#numéro)")
        return False

    issue_num = match.group(1)
    state = get_issue_state(issue_num)

    if not state:
        error(file_path, line_num, f"L'issue #{issue_num} n'existe pas.")
        return False

    if state == ISSUE_CLOSED:
        error(file_path, line_num, f"L'issue #{issue_num} est fermée.")
        return False

    print(f"OK : {file_path}:{line_num} → issue #{issue_num} ouverte.")
    return True


all_ok = True

for line in find_todos():
    # grep renvoie des lignes de la forme "fichier:numero:contenu"
    parts = line.split(":", 2)
    if len(parts) < 3:
        continue

    file_path, line_num, content = parts
    if not check_todo(file_path, line_num, content):
        all_ok = False

if not all_ok:
    sys.exit(1)

print("Tous les TODOs sont associés à une issue ouverte.")
