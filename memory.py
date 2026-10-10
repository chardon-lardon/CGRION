"""Historique local sauvegardé après chaque échange."""
import json
from datetime import datetime
from uuid import uuid4
from config import DATA_DIR

HISTORY_FILE = DATA_DIR / "history.json"
session_id = str(uuid4())


def load_history():
    """Lit les échanges et signale un fichier endommagé sans l'écraser."""
    if not HISTORY_FILE.exists():
        return []
    items = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    if not isinstance(items, list) or any(
        not isinstance(item, dict) or
        not all(isinstance(item.get(key), str) for key in ("message", "response", "date", "session"))
        for item in items
    ):
        raise ValueError("Le format de l'historique est invalide.")
    return items


def remember(message, response):
    """Ajoute un échange puis remplace le fichier de façon atomique."""
    items = load_history()
    items.append({"message": message, "response": response,
                  "date": datetime.now().astimezone().isoformat(timespec="seconds"),
                  "session": session_id})
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = HISTORY_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(HISTORY_FILE)


def new_session():
    """Commence une nouvelle conversation sans supprimer les échanges passés."""
    global session_id
    session_id = str(uuid4())


def clear_history():
    """Supprime tous les échanges sauvegardés."""
    HISTORY_FILE.unlink(missing_ok=True)
