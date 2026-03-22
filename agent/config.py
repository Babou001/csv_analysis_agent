"""
Configuration de l'agent.

Centralise les paramètres et le chargement des prompts.
"""

from pathlib import Path


# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DATA_DIR = PROJECT_ROOT / "data"


def load_prompt(prompt_name: str) -> str:
    """
    Charge un prompt depuis le dossier prompts/.

    Args:
        prompt_name: Nom du fichier (sans l'extension .txt)

    Returns:
        Le contenu du prompt

    Raises:
        FileNotFoundError: Si le prompt n'existe pas
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt '{prompt_name}' non trouvé à {prompt_path}")

    return prompt_path.read_text(encoding="utf-8").strip()


def get_system_prompt() -> str:
    """
    Retourne le prompt système pour l'agent.

    Returns:
        Le prompt système
    """
    return load_prompt("system")


# Configuration du LLM
LLM_CONFIG = {
    "model": "gemini-2.5-flash",
    "temperature": 0,
}

# Configuration de l'agent
AGENT_CONFIG = {
    "max_iterations": 10,  # Nombre max de cycles agent→tools
    "timeout": 120,  # Timeout en secondes
}
