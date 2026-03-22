"""
Interface Streamlit pour l'agent DataFrame.

Lance avec: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from agent.tools import load_dataframe, get_dataframe
from agent.graph import graph


# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="Agent DataFrame",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== HELPER FUNCTIONS ====================

def extract_final_response(state):
    """
    Extrait la réponse finale de l'agent depuis le state.
    """
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "content"):
        content = last_message.content

        # Si le content est une liste (format structured output)
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


def run_agent_query(question):
    """
    Exécute une question avec l'agent et retourne la réponse.

    Args:
        question: La question de l'utilisateur

    Returns:
        str: La réponse de l'agent
    """
    initial_state = {"messages": [("user", question)]}

    final_state = None
    for event in graph.stream(initial_state, stream_mode="values"):
        final_state = event

    if final_state:
        return extract_final_response(final_state)

    return "❌ Erreur: Aucune réponse générée."


# ==================== SESSION STATE ====================

# Initialise le session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False

if "df_info" not in st.session_state:
    st.session_state.df_info = None


# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("📊 Agent DataFrame")
    st.markdown("---")

    st.header("📂 Chargement des données")

    # Option 1: Fichier uploadé
    uploaded_file = st.file_uploader(
        "Upload un fichier CSV",
        type=["csv"],
        help="Charge ton propre fichier CSV"
    )

    # Option 2: Fichier par défaut
    st.markdown("**OU**")

    default_file = Path("data/ventes.csv")
    if default_file.exists():
        if st.button("📁 Utiliser le fichier d'exemple", use_container_width=True):
            try:
                df = load_dataframe(str(default_file))
                st.session_state.df_loaded = True
                st.session_state.df_info = {
                    "filename": "ventes.csv",
                    "rows": len(df),
                    "cols": len(df.columns),
                    "columns": df.columns.tolist()
                }
                st.success("✅ Fichier d'exemple chargé !")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

    # Traite l'upload
    if uploaded_file is not None:
        try:
            # Sauvegarde temporaire
            temp_path = f"data/temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Charge le DataFrame
            df = load_dataframe(temp_path)
            st.session_state.df_loaded = True
            st.session_state.df_info = {
                "filename": uploaded_file.name,
                "rows": len(df),
                "cols": len(df.columns),
                "columns": df.columns.tolist()
            }
            st.success("✅ Fichier chargé avec succès !")
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {str(e)}")

    st.markdown("---")

    # Affiche les infos du DataFrame chargé
    if st.session_state.df_loaded:
        st.header("📋 Informations")
        info = st.session_state.df_info

        st.metric("Fichier", info["filename"])
        st.metric("Lignes", info["rows"])
        st.metric("Colonnes", info["cols"])

        with st.expander("📋 Liste des colonnes"):
            for col in info["columns"]:
                st.write(f"• {col}")

        if st.button("🗑️ Réinitialiser", use_container_width=True):
            st.session_state.messages = []
            st.session_state.df_loaded = False
            st.session_state.df_info = None
            st.rerun()

    st.markdown("---")

    # Aide
    with st.expander("💡 Exemples de questions"):
        st.markdown("""
        - Montre-moi les premières lignes
        - Quelle est la moyenne des prix ?
        - Combien y a-t-il de produits par catégorie ?
        - Filtre les produits qui coûtent plus de 100€
        - Quel est le produit le plus cher ?
        - Donne-moi les statistiques de la colonne quantite
        """)


# ==================== MAIN CONTENT ====================

# Header
st.title("🤖 Agent d'Analyse de Données")
st.markdown("Pose des questions sur tes données en langage naturel !")

# Vérifie si un DataFrame est chargé
if not st.session_state.df_loaded:
    st.info("👈 Commence par charger un fichier CSV depuis la barre latérale")

    # Aperçu du dataset d'exemple
    default_file = Path("data/ventes.csv")
    if default_file.exists():
        st.markdown("### 👀 Aperçu du fichier d'exemple")
        df_preview = pd.read_csv(default_file)
        st.dataframe(df_preview, use_container_width=True)

    st.stop()


# Zone de conversation
st.markdown("### 💬 Conversation")

# Affiche l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Zone de saisie
if prompt := st.chat_input("Pose ta question sur les données..."):
    # Ajoute le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Affiche le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génère la réponse
    with st.chat_message("assistant"):
        with st.spinner("🤔 Réflexion en cours..."):
            try:
                response = run_agent_query(prompt)
                st.markdown(response)

                # Ajoute la réponse à l'historique
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                error_msg = f"❌ Erreur: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })


# ==================== FOOTER ====================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Créé avec ❤️ en utilisant LangChain, LangGraph et Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
