"""
Connexion au LLM (Google Gemini) via LangChain.

Pourquoi ce fichier ?
→ On isole la config du LLM dans un seul endroit.
  Si demain tu veux passer à OpenAI ou Ollama,
  tu changes UNIQUEMENT ce fichier.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.config import LLM_CONFIG

# Charge les variables d'environnement depuis .env
load_dotenv()

def get_llm():
    """
    Crée et retourne une instance du LLM Gemini.

    Configuration centralisée dans agent/config.py
    """
    llm = ChatGoogleGenerativeAI(
        model=LLM_CONFIG["model"],
        temperature=LLM_CONFIG["temperature"],
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    return llm


# --- Test rapide ---
if __name__ == "__main__":
    llm = get_llm()

    # .invoke() envoie un message au LLM et attend la réponse
    response = llm.invoke("Dis-moi bonjour en français, en une phrase.")

    # response est un objet AIMessage, .content contient le texte
    print(response.content)
