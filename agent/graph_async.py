"""
Version asynchrone du graphe LangGraph.

Améliore la scalabilité et les performances pour un déploiement multi-utilisateurs.
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent.llm import get_llm
from agent.tools import TOOLS
from agent.config import get_system_prompt


# ==================== STATE ====================

class State(TypedDict):
    """Structure de données qui circule dans le graphe."""
    messages: Annotated[list, add_messages]


# ==================== NŒUDS ASYNC ====================

async def agent_node(state: State) -> State:
    """
    Nœud Agent asynchrone : Le LLM réfléchit et décide quoi faire.

    Version async pour supporter plusieurs requêtes simultanées.
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
        if hasattr(msg, 'type') and msg.type == "system":
            has_system_message = True
            break

    # Si aucun message système, on en ajoute un
    if not has_system_message:
        from langchain_core.messages import SystemMessage
        messages = [SystemMessage(content=system_message)] + messages

    # Appel asynchrone au LLM
    response = await llm_with_tools.ainvoke(messages)

    return {"messages": [response]}


# Le nœud Tools reste synchrone (pandas n'est pas async)
tools_node = ToolNode(TOOLS)


# ==================== ROUTAGE ====================

def should_continue(state: State) -> str:
    """Fonction de routage (reste synchrone)."""
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# ==================== CONSTRUCTION DU GRAPHE ====================

def create_async_graph():
    """
    Crée et compile le graphe asynchrone de l'agent.

    Identique au graphe synchrone, mais avec des nœuds async.
    """
    workflow = StateGraph(State)

    # Ajoute les nœuds
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    # Ajoute les arêtes
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    return workflow.compile()


# Instance globale du graphe async
graph_async = create_async_graph()


# ==================== HELPER ASYNC ====================

async def run_agent_async(user_message: str, verbose: bool = False) -> str:
    """
    Fonction helper asynchrone pour exécuter l'agent.

    Args:
        user_message: La question de l'utilisateur
        verbose: Si True, affiche les étapes

    Returns:
        La réponse finale de l'agent
    """
    initial_state = {
        "messages": [("user", user_message)]
    }

    if verbose:
        print("🤖 Agent async en cours...\n")

    final_state = None
    async for event in graph_async.astream(initial_state, stream_mode="values"):
        final_state = event

    # Récupère la réponse finale
    if final_state:
        last_message = final_state["messages"][-1]
        return last_message.content

    return "❌ Erreur: Aucune réponse générée."


# ==================== TEST ====================

if __name__ == "__main__":
    import asyncio
    from agent.tools import load_dataframe

    async def test_async():
        """Test du graphe async"""
        print("📂 Chargement du DataFrame...")
        load_dataframe("data/ventes.csv")
        print("✅ DataFrame chargé\n")

        print("=" * 60)
        print("TEST ASYNC")
        print("=" * 60)

        # Test avec plusieurs questions en parallèle
        questions = [
            "Quel est le produit le plus cher ?",
            "Combien y a-t-il de produits par catégorie ?",
        ]

        # Lance les requêtes en parallèle (async concurrency)
        tasks = [run_agent_async(q, verbose=False) for q in questions]
        responses = await asyncio.gather(*tasks)

        for question, response in zip(questions, responses):
            print(f"\n💬 Question: {question}")
            print(f"🤖 Réponse: {response}")

        print("\n" + "=" * 60)
        print("✅ Test async terminé !")

    # Lance le test async
    asyncio.run(test_async())
