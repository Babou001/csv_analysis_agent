"""
Outils pandas pour l'agent.

Chaque outil est une fonction Python transformée en "tool" que le LLM peut appeler.
Le décorateur @tool fait la magie :
- Il indique au LLM ce que fait la fonction (via la docstring)
- Il gère automatiquement les paramètres et le retour
"""

import pandas as pd
from typing import Optional
from langchain_core.tools import tool


# Variable globale pour stocker le DataFrame
# (On verra une meilleure approche avec le State dans l'étape 3)
_current_df: Optional[pd.DataFrame] = None


def load_dataframe(file_path: str) -> pd.DataFrame:
    """
    Charge un CSV et le stocke comme DataFrame actif.
    Cette fonction n'est PAS un tool, c'est juste une fonction helper.
    """
    global _current_df
    _current_df = pd.read_csv(file_path)
    return _current_df


def get_dataframe() -> pd.DataFrame:
    """
    Retourne le DataFrame actuel.
    Lève une erreur si aucun DataFrame n'est chargé.
    """
    if _current_df is None:
        raise ValueError("Aucun DataFrame chargé. Utilisez load_dataframe() d'abord.")
    return _current_df


# ==================== LES TOOLS ====================
# Ce sont les outils que le LLM va pouvoir utiliser


@tool
def get_head(n: int = 5) -> str:
    """
    Affiche les n premières lignes du DataFrame.

    Args:
        n: Nombre de lignes à afficher (par défaut 5)

    Returns:
        Les premières lignes du DataFrame formatées en texte

    Utilise cet outil quand l'utilisateur veut voir un aperçu des données.
    """
    df = get_dataframe()
    return df.head(n).to_string()


@tool
def get_info() -> str:
    """
    Retourne les informations sur le DataFrame :
    - Nombre de lignes et colonnes
    - Nom des colonnes
    - Types de données
    - Valeurs manquantes

    Utilise cet outil quand l'utilisateur veut comprendre la structure des données.
    """
    df = get_dataframe()

    # Collecte les infos
    info_parts = [
        f"Shape: {df.shape[0]} lignes × {df.shape[1]} colonnes",
        f"\nColonnes: {', '.join(df.columns.tolist())}",
        f"\nTypes de données:\n{df.dtypes.to_string()}",
        f"\nValeurs manquantes:\n{df.isnull().sum().to_string()}",
    ]

    return "\n".join(info_parts)


@tool
def calculate_stats(column: str) -> str:
    """
    Calcule les statistiques descriptives pour une colonne numérique.

    Args:
        column: Nom de la colonne à analyser

    Returns:
        Statistiques (moyenne, médiane, min, max, etc.)

    Utilise cet outil pour des calculs comme : moyenne, somme, min, max, écart-type.
    """
    df = get_dataframe()

    if column not in df.columns:
        return f"Erreur: La colonne '{column}' n'existe pas. Colonnes disponibles: {', '.join(df.columns)}"

    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Erreur: La colonne '{column}' n'est pas numérique. Type: {df[column].dtype}"

    stats = df[column].describe()
    return f"Statistiques pour '{column}':\n{stats.to_string()}"


@tool
def filter_data(column: str, operator: str, value: str) -> str:
    """
    Filtre le DataFrame selon une condition.

    Args:
        column: Nom de la colonne
        operator: Opérateur de comparaison ('==', '>', '<', '>=', '<=', '!=')
        value: Valeur de comparaison

    Returns:
        Les lignes filtrées

    Exemples d'utilisation :
    - filter_data("prix", ">", "100") → produits > 100€
    - filter_data("categorie", "==", "Electronique") → produits électroniques
    """
    df = get_dataframe()

    if column not in df.columns:
        return f"Erreur: La colonne '{column}' n'existe pas."

    # Convertit la valeur au bon type
    try:
        if pd.api.types.is_numeric_dtype(df[column]):
            value = float(value)
    except:
        pass  # Garde value comme string

    # Applique le filtre
    try:
        if operator == "==":
            filtered = df[df[column] == value]
        elif operator == ">":
            filtered = df[df[column] > value]
        elif operator == "<":
            filtered = df[df[column] < value]
        elif operator == ">=":
            filtered = df[df[column] >= value]
        elif operator == "<=":
            filtered = df[df[column] <= value]
        elif operator == "!=":
            filtered = df[df[column] != value]
        else:
            return f"Erreur: Opérateur '{operator}' non supporté."

        return f"Résultats ({len(filtered)} lignes):\n{filtered.to_string()}"

    except Exception as e:
        return f"Erreur lors du filtrage: {str(e)}"


@tool
def group_by(column: str, agg_column: str, agg_func: str = "sum") -> str:
    """
    Regroupe les données et applique une fonction d'agrégation.

    Args:
        column: Colonne de regroupement
        agg_column: Colonne à agréger
        agg_func: Fonction d'agrégation ('sum', 'mean', 'count', 'min', 'max')

    Returns:
        Les résultats agrégés

    Exemples :
    - group_by("categorie", "prix", "sum") → total des prix par catégorie
    - group_by("categorie", "produit", "count") → nombre de produits par catégorie
    """
    df = get_dataframe()

    if column not in df.columns:
        return f"Erreur: La colonne '{column}' n'existe pas."

    if agg_column not in df.columns:
        return f"Erreur: La colonne '{agg_column}' n'existe pas."

    try:
        if agg_func == "sum":
            result = df.groupby(column)[agg_column].sum()
        elif agg_func == "mean":
            result = df.groupby(column)[agg_column].mean()
        elif agg_func == "count":
            result = df.groupby(column)[agg_column].count()
        elif agg_func == "min":
            result = df.groupby(column)[agg_column].min()
        elif agg_func == "max":
            result = df.groupby(column)[agg_column].max()
        else:
            return f"Erreur: Fonction '{agg_func}' non supportée."

        return f"Résultats du groupby:\n{result.to_string()}"

    except Exception as e:
        return f"Erreur lors de l'agrégation: {str(e)}"


# ==================== LISTE DES TOOLS ====================
# Cette liste sera utilisée par l'agent

TOOLS = [
    get_head,
    get_info,
    calculate_stats,
    filter_data,
    group_by,
]


# ==================== TEST ====================
if __name__ == "__main__":
    """Test rapide des tools"""

    # Charge le CSV de test
    print("📂 Chargement du DataFrame...")
    df = load_dataframe("data/ventes.csv")
    print(f"✅ {len(df)} lignes chargées\n")

    # Teste chaque tool
    print("=" * 60)
    print("TEST 1: get_head()")
    print("=" * 60)
    print(get_head.invoke({"n": 3}))

    print("\n" + "=" * 60)
    print("TEST 2: get_info()")
    print("=" * 60)
    print(get_info.invoke({}))

    print("\n" + "=" * 60)
    print("TEST 3: calculate_stats('prix')")
    print("=" * 60)
    print(calculate_stats.invoke({"column": "prix"}))

    print("\n" + "=" * 60)
    print("TEST 4: filter_data('categorie', '==', 'Electronique')")
    print("=" * 60)
    print(filter_data.invoke({"column": "categorie", "operator": "==", "value": "Electronique"}))

    print("\n" + "=" * 60)
    print("TEST 5: group_by('categorie', 'prix', 'sum')")
    print("=" * 60)
    print(group_by.invoke({"column": "categorie", "agg_column": "prix", "agg_func": "sum"}))

    print("\n✅ Tous les tests passés !")
