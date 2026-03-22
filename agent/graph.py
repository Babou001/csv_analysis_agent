"""
Graphe LangGraph : Le cerveau de l'agent.

Ce fichier crée un graphe qui orchestre :
1. L'agent LLM (décide quoi faire)
2. Les tools pandas (exécutent des actions)
3. Le cycle agent → tools → agent jusqu'à la réponse finale
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent.llm import get_llm
from agent.tools import TOOLS
from agent.config import get_system_prompt


# ==================== 1. LE STATE ====================
# Le State est la "mémoire" de l'agent pendant la conversation

class State(TypedDict):
    """
    Structure de données qui circule dans le graphe.

    - messages: Historique de la conversation (utilisateur + LLM + tools)

    Le type Annotated[list, add_messages] est spécial :
    - Il dit à LangGraph de TOUJOURS AJOUTER les nouveaux messages
      à la liste existante (au lieu de la remplacer)
    - Ça crée automatiquement une "mémoire" de la conversation
    """
    messages: Annotated[list, add_messages]


# ==================== 2. LES NŒUDS ====================
# Un nœud est une fonction qui prend le State et retourne un State modifié

def agent_node(state: State) -> State:
    """
    Nœud Agent : Le LLM réfléchit et décide quoi faire.

    Le LLM peut :
    - Appeler un tool (si besoin de données pandas)
    - Répondre directement (si il a assez d'infos)

    Comment ça marche ?
    1. On donne au LLM la liste des tools disponibles (.bind_tools)
    2. Le LLM analyse les messages de la conversation
    3. Il décide : "J'ai besoin du tool X" OU "Je peux répondre"
    4. Sa décision est ajoutée aux messages
    """
    # Charge le system prompt depuis le fichier
    system_message = get_system_prompt()

    # Récupère le LLM et lui donne accès aux tools
    llm = get_llm()
    llm_with_tools = llm.bind_tools(TOOLS)

    # Ajoute le system message au début si c'est le premier appel
    messages = state["messages"]

    # Vérifie si un message système existe déjà
    has_system_message = False
    for msg in messages:
        # Les messages LangChain ont un attribut 'type'
        if hasattr(msg, 'type') and msg.type == "system":
            has_system_message = True
            break

    # Si aucun message système, on en ajoute un
    if not has_system_message:
        from langchain_core.messages import SystemMessage
        messages = [SystemMessage(content=system_message)] + messages

    # Le LLM analyse la conversation et prend une décision
    response = llm_with_tools.invoke(messages)

    # Retourne le State avec la réponse du LLM ajoutée
    return {"messages": [response]}


# Le nœud Tools est géré automatiquement par LangGraph
# ToolNode exécute le tool demandé par le LLM et retourne le résultat
tools_node = ToolNode(TOOLS)


# ==================== 3. LA LOGIQUE DE ROUTAGE ====================

def should_continue(state: State) -> str:
    """
    Fonction de routage : Décide si on continue ou si on termine.

    Regarder le dernier message :
    - Si c'est un tool_call (appel de tool) → on va vers "tools"
    - Sinon (réponse finale du LLM) → on termine (END)

    C'est cette fonction qui crée le cycle :
    agent → tools → agent → tools → ... → END
    """
    last_message = state["messages"][-1]

    # Si le LLM veut appeler un tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Sinon, on a terminé
    return END


# ==================== 4. CONSTRUCTION DU GRAPHE ====================

def create_graph():
    """
    Crée et compile le graphe de l'agent.

    Structure du graphe :

    START
      ↓
    agent ←──┐
      │      │
      ↓      │
    tools ──┘
      │
      ↓
     END

    Explication :
    1. On commence toujours par le nœud "agent"
    2. L'agent décide : appeler un tool ou répondre
    3. Si tool : on va vers "tools", puis on retourne à "agent"
    4. Si réponse : on termine (END)
    """
    # Initialise le graphe avec notre State
    workflow = StateGraph(State)

    # Ajoute les nœuds
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    # Ajoute l'arête de départ : START → agent
    workflow.add_edge(START, "agent")

    # Ajoute l'arête conditionnelle : agent → tools OU END
    workflow.add_conditional_edges(
        "agent",           # Depuis le nœud "agent"
        should_continue,   # Utilise cette fonction pour décider
    )

    # Ajoute l'arête de retour : tools → agent
    workflow.add_edge("tools", "agent")

    # Compile le graphe (le rend exécutable)
    return workflow.compile()


# ==================== 5. INSTANCE GLOBALE ====================
# On crée une instance du graphe qu'on pourra utiliser partout

graph = create_graph()


# ==================== 6. HELPER POUR INVOKER LE GRAPHE ====================

def run_agent(user_message: str, verbose: bool = True) -> str:
    """
    Fonction helper pour exécuter l'agent facilement.

    Args:
        user_message: La question de l'utilisateur
        verbose: Si True, affiche les étapes intermédiaires

    Returns:
        La réponse finale de l'agent
    """
    # Prépare le state initial avec le message de l'utilisateur
    initial_state = {
        "messages": [("user", user_message)]
    }

    # Exécute le graphe
    if verbose:
        print("🤖 Agent en cours d'exécution...\n")

    # stream() permet de voir chaque étape en temps réel
    for event in graph.stream(initial_state, stream_mode="values"):
        # Affiche le dernier message à chaque étape
        if verbose:
            last_message = event["messages"][-1]

            # Message utilisateur
            if hasattr(last_message, "type") and last_message.type == "human":
                print(f"👤 Utilisateur: {last_message.content}\n")

            # Message LLM
            elif hasattr(last_message, "type") and last_message.type == "ai":
                # Si le LLM appelle un tool
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"🔧 Tool appelé: {tool_call['name']}")
                        print(f"   Arguments: {tool_call['args']}\n")
                # Si le LLM répond
                elif last_message.content:
                    print(f"🤖 Agent: {last_message.content}\n")

            # Résultat d'un tool
            elif hasattr(last_message, "type") and last_message.type == "tool":
                print(f"📊 Résultat du tool '{last_message.name}':")
                # Limite l'affichage pour ne pas polluer le terminal
                content_preview = last_message.content[:200]
                if len(last_message.content) > 200:
                    content_preview += "..."
                print(f"   {content_preview}\n")

    # Récupère la réponse finale
    final_state = event
    final_message = final_state["messages"][-1]

    return final_message.content


# ==================== 7. TEST ====================

if __name__ == "__main__":
    """Test du graphe avec une conversation simple"""

    from agent.tools import load_dataframe

    # Charge le DataFrame de test
    print("📂 Chargement du DataFrame...")
    load_dataframe("data/ventes.csv")
    print("✅ DataFrame chargé\n")

    print("=" * 60)
    print("TEST DU GRAPHE")
    print("=" * 60)
    print()

    # Question 1 : Simple (nécessite get_head)
    print("🔹 Question 1: Aperçu des données")
    print("-" * 60)
    response = run_agent("Montre-moi les 3 premières lignes des données")
    print(f"\n✅ Réponse finale:\n{response}\n")

    print("\n" + "=" * 60)
    print()

    # Question 2 : Calcul (nécessite calculate_stats)
    print("🔹 Question 2: Statistiques")
    print("-" * 60)
    response = run_agent("Quelle est la moyenne des prix ?")
    print(f"\n✅ Réponse finale:\n{response}\n")

    print("\n" + "=" * 60)
    print()

    # Question 3 : Complexe (nécessite filter_data puis group_by)
    print("🔹 Question 3: Analyse complexe")
    print("-" * 60)
    response = run_agent("Combien coûtent les produits électroniques en total ?")
    print(f"\n✅ Réponse finale:\n{response}\n")

    print("=" * 60)
    print("✅ Tests terminés !")
