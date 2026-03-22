#!/usr/bin/env python3
"""
Interface CLI pour l'agent DataFrame.

Lance ce fichier pour interagir avec l'agent dans le terminal.
Usage: python app_cli.py
"""

import sys
import os
from pathlib import Path

from agent.tools import load_dataframe
from agent.graph import graph


def print_banner():
    """Affiche le banner de l'application"""
    print("\n" + "=" * 60)
    print("📊 Agent DataFrame - Analyse de données avec IA")
    print("=" * 60)
    print()


def load_csv_interactive():
    """
    Demande à l'utilisateur de charger un CSV.
    Retourne le DataFrame ou None si échec.
    """
    print("📂 Charge un fichier CSV")
    print("-" * 60)

    # Suggère le fichier par défaut
    default_file = "data/ventes.csv"
    if Path(default_file).exists():
        print(f"Fichier par défaut disponible: {default_file}")
        use_default = input("Utiliser ce fichier ? (O/n): ").strip().lower()

        if use_default in ["", "o", "oui", "y", "yes"]:
            file_path = default_file
        else:
            file_path = input("Chemin du fichier CSV: ").strip()
    else:
        file_path = input("Chemin du fichier CSV: ").strip()

    # Charge le fichier
    try:
        df = load_dataframe(file_path)
        print(f"\n✅ DataFrame chargé avec succès !")
        print(f"   📊 {len(df)} lignes × {len(df.columns)} colonnes")
        print(f"   📋 Colonnes: {', '.join(df.columns.tolist())}")
        print()
        return df
    except FileNotFoundError:
        print(f"\n❌ Erreur: Le fichier '{file_path}' n'existe pas.")
        return None
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement: {str(e)}")
        return None


def extract_final_response(state):
    """
    Extrait la réponse finale de l'agent depuis le state.

    Args:
        state: Le state final retourné par le graphe

    Returns:
        La réponse en texte (str)
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Gère différents formats de message
    if hasattr(last_message, "content"):
        content = last_message.content

        # Si le content est une liste (format structured output)
        if isinstance(content, list):
            # Extrait le texte de chaque élément
            text_parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, str):
                    text_parts.append(item)
            return "\n".join(text_parts)

        # Si c'est directement du texte
        return str(content)

    return "Aucune réponse générée."


def chat_loop():
    """
    Boucle de conversation avec l'agent.
    """
    print("💬 Mode conversation activé")
    print("-" * 60)
    print("Commandes spéciales:")
    print("  • 'quit' ou 'exit' : Quitter")
    print("  • 'clear' : Nettoyer l'écran")
    print("  • 'help' : Afficher l'aide")
    print()

    while True:
        try:
            # Demande la question
            user_input = input("💬 Toi: ").strip()

            # Gère les commandes spéciales
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 À bientôt !")
                break

            if user_input.lower() == "clear":
                os.system('clear' if os.name != 'nt' else 'cls')
                print_banner()
                continue

            if user_input.lower() == "help":
                print("\n📖 Aide")
                print("-" * 60)
                print("Exemples de questions:")
                print("  • Montre-moi les premières lignes")
                print("  • Quelle est la moyenne des prix ?")
                print("  • Combien y a-t-il de produits par catégorie ?")
                print("  • Filtre les produits qui coûtent plus de 100€")
                print("  • Quel est le produit le plus cher ?")
                print()
                continue

            # Ignore les entrées vides
            if not user_input:
                continue

            # Exécute l'agent
            print("\n🤖 Agent:", end=" ", flush=True)

            # Prépare le state
            initial_state = {
                "messages": [("user", user_input)]
            }

            # Exécute le graphe (sans verbose pour une sortie propre)
            final_state = None
            for event in graph.stream(initial_state, stream_mode="values"):
                final_state = event

            # Extrait et affiche la réponse
            if final_state:
                response = extract_final_response(final_state)
                print(response)
            else:
                print("❌ Erreur: Aucune réponse générée.")

            print()  # Ligne vide pour la lisibilité

        except KeyboardInterrupt:
            print("\n\n👋 Interruption détectée. À bientôt !")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
            print("Réessaye avec une autre question.\n")


def main():
    """Point d'entrée principal"""
    print_banner()

    # Charge le CSV
    df = load_csv_interactive()

    if df is None:
        print("\n⚠️  Impossible de continuer sans données.")
        print("Assure-toi que le fichier CSV existe et réessaye.")
        sys.exit(1)

    # Lance la boucle de conversation
    chat_loop()


if __name__ == "__main__":
    main()
