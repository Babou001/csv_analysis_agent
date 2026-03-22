#!/usr/bin/env python3
"""
Script de test pour l'interface CLI (mode automatique).
"""

from agent.tools import load_dataframe
from agent.graph import graph

def extract_final_response(state):
    """Extrait la réponse finale"""
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "content"):
        content = last_message.content

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, str):
                    text_parts.append(item)
            return "\n".join(text_parts)

        return str(content)

    return "Aucune réponse générée."


def test_question(question):
    """Teste une question avec l'agent"""
    print(f"\n{'='*60}")
    print(f"💬 Question: {question}")
    print('='*60)

    initial_state = {"messages": [("user", question)]}

    final_state = None
    for event in graph.stream(initial_state, stream_mode="values"):
        final_state = event

    if final_state:
        response = extract_final_response(final_state)
        print(f"\n🤖 Réponse:\n{response}")
    else:
        print("❌ Erreur: Aucune réponse")


def main():
    print("\n" + "=" * 60)
    print("🧪 Test de l'interface CLI")
    print("=" * 60)

    # Charge le dataset
    print("\n📂 Chargement du dataset...")
    df = load_dataframe("data/ventes.csv")
    print(f"✅ {len(df)} lignes chargées\n")

    # Liste de questions à tester
    questions = [
        "Montre-moi les 3 premières lignes",
        "Quelle est la moyenne des prix ?",
        "Combien y a-t-il de produits par catégorie ?",
        "Quel est le produit le plus cher ?",
    ]

    # Teste chaque question
    for question in questions:
        test_question(question)

    print("\n" + "=" * 60)
    print("✅ Tests terminés !")
    print("=" * 60)


if __name__ == "__main__":
    main()
