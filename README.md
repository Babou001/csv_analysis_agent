# 📊 Agent DataFrame - Analyse de données avec IA

Un agent intelligent qui analyse tes données CSV en langage naturel grâce à LangChain, LangGraph et Google Gemini.

> ⚠️ **Note importante** : Ce projet est un **proof of concept (POC)** et une base d'apprentissage pour comprendre LangChain et LangGraph. Il n'est **pas production-ready** et nécessiterait plusieurs améliorations pour une utilisation à grande échelle (voir section [Limitations et évolutions](#-limitations-et-évolutions-futures)).

## 🎯 Fonctionnalités

- 💬 **Conversation naturelle** : Pose des questions en français sur tes données
- 🧠 **Agent intelligent** : Utilise LangGraph pour orchestrer l'analyse
- 🔧 **Outils pandas** : Filtrage, statistiques, groupements automatiques
- 🖥️ **Interface CLI** : Utilise l'agent dans le terminal
- 🌐 **Interface Web** : Belle interface Streamlit pour le web
- 🔒 **Sécurisé** : Clé API jamais exposée grâce au `.gitignore`
- 🐳 **Docker ready** : Déploiement facile avec Docker et docker-compose
- ⚡ **Async support** : Version asynchrone pour meilleure scalabilité

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  TOI (Question)                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              LANGGRAPH (Orchestration)                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Agent LLM (Gemini)                             │   │
│  │  → Comprend la question                         │   │
│  │  → Décide quel tool utiliser                    │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                       │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Tools Pandas                                    │  │
│  │  • get_head()        → Aperçu                    │  │
│  │  • get_info()        → Structure                 │  │
│  │  • calculate_stats() → Statistiques              │  │
│  │  • filter_data()     → Filtrage                  │  │
│  │  • group_by()        → Agrégation                │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                       │
│                 ▼ (cycle jusqu'à réponse finale)       │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              RÉPONSE EN FRANÇAIS                        │
└─────────────────────────────────────────────────────────┘
```

## 📦 Installation

### 1. Clone le projet

```bash
git clone <ton-repo>
cd Agent-dataframe
```

### 2. Crée un environnement virtuel

```bash
# Crée l'environnement
python -m venv venv

# Active-le
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows
```

### 3. Installe les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configure ta clé API Gemini

1. Va sur [Google AI Studio](https://aistudio.google.com)
2. Crée une clé API (gratuite)
3. Copie `.env.example` vers `.env`:
   ```bash
   cp .env.example .env
   ```
4. Ouvre `.env` et ajoute ta clé:
   ```
   GOOGLE_API_KEY=ta_clé_ici
   ```

## 🐳 Installation avec Docker (Recommandé)

Docker garantit que l'application fonctionne **de manière identique** sur tous les environnements (Linux, Mac, Windows).

### Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Démarrage rapide

```bash
# 1. Clone le projet
git clone <ton-repo>
cd Agent-dataframe

# 2. Configure ta clé API
cp .env.example .env
# Édite .env et ajoute ta clé GOOGLE_API_KEY

# 3. Lance avec Docker Compose
docker-compose up -d

# 4. Accède à Streamlit
# Ouvre http://localhost:8501 dans ton navigateur
```

### Commandes Docker utiles

```bash
# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Rebuild après modification du code
docker-compose up -d --build

# Shell dans le container
docker-compose exec agent-dataframe /bin/bash
```

### Utilisation avec Makefile (encore plus simple)

```bash
# Affiche l'aide
make help

# Construit l'image
make build

# Lance les services
make up

# Voir les logs
make logs

# Arrête tout
make down

# Nettoie
make clean
```

## 🚀 Utilisation

### Interface CLI (Terminal)

```bash
python app_cli.py
```

**Exemple de session :**
```
📊 Agent DataFrame - Analyse de données avec IA
============================================================

📂 Charge un fichier CSV
Utiliser data/ventes.csv ? (O/n): O

✅ DataFrame chargé avec succès !
   📊 10 lignes × 5 colonnes

💬 Toi: Quelle est la moyenne des prix ?
🤖 Agent: La moyenne des prix est de 264,50€.

💬 Toi: Montre-moi les produits électroniques
🤖 Agent: Voici les produits de la catégorie Electronique...
```

### Interface Web (Streamlit)

```bash
streamlit run app_streamlit.py
```

Ouvre ton navigateur sur `http://localhost:8501`

**Fonctionnalités :**
- 📂 Upload de fichiers CSV
- 💬 Chat interactif
- 📊 Visualisation du DataFrame
- 🔄 Historique des conversations

## 📁 Structure du projet

```
Agent-dataframe/
├── .env                     # Ta clé API (JAMAIS commit)
├── .env.example             # Template pour la clé API
├── .gitignore               # Fichiers à ignorer par Git
├── .dockerignore            # Fichiers à ignorer par Docker
├── README.md                # Ce fichier
├── requirements.txt         # Dépendances Python
│
├── Dockerfile               # Image Docker (Python 3.12)
├── docker-compose.yml       # Orchestration Docker
├── Makefile                 # Commandes simplifiées
│
├── app_cli.py               # Interface terminal
├── app_streamlit.py         # Interface web Streamlit
├── check_setup.py           # Vérification de l'installation
├── test_cli.py              # Tests (sans appels LLM)
│
├── agent/
│   ├── __init__.py
│   ├── config.py            # Configuration centralisée
│   ├── llm.py               # Connexion au LLM Gemini
│   ├── tools.py             # Outils pandas (5 tools)
│   ├── graph.py             # Graphe LangGraph (synchrone)
│   └── graph_async.py       # Graphe LangGraph (asynchrone)
│
├── prompts/
│   └── system.txt           # Prompt système (externalisé)
│
└── data/
    └── ventes.csv           # Dataset d'exemple
```

## 🛠️ Les outils pandas disponibles

L'agent dispose de 5 outils pour analyser tes données :

| Outil | Description | Exemple de question |
|-------|-------------|---------------------|
| `get_head()` | Affiche les premières lignes | "Montre-moi un aperçu des données" |
| `get_info()` | Structure du DataFrame | "Quelles sont les colonnes disponibles ?" |
| `calculate_stats()` | Statistiques (moyenne, min, max...) | "Quelle est la moyenne des prix ?" |
| `filter_data()` | Filtre selon une condition | "Montre les produits > 100€" |
| `group_by()` | Regroupe et agrège | "Total des prix par catégorie ?" |

## 💡 Exemples de questions

```
✅ Questions simples
• Montre-moi les premières lignes
• Combien y a-t-il de lignes dans les données ?
• Quelles sont les colonnes disponibles ?

✅ Statistiques
• Quelle est la moyenne des prix ?
• Quel est le produit le plus cher ?
• Donne-moi les statistiques de la colonne quantite

✅ Filtres
• Montre-moi les produits électroniques
• Filtre les produits qui coûtent plus de 100€
• Quels produits ont une quantité supérieure à 20 ?

✅ Agrégations
• Combien y a-t-il de produits par catégorie ?
• Quel est le total des prix par catégorie ?
• Quelle est la quantité moyenne par catégorie ?
```

## 🧪 Tests

### Tester les outils pandas individuellement

```bash
python agent/tools.py
```

### Tester le graphe LangGraph

```bash
python -m agent.graph
```

### Tester l'interface CLI (mode automatique)

```bash
python test_cli.py
```

## 🔧 Configuration avancée

### Changer de modèle LLM

Édite `agent/llm.py` :

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Change ici
    temperature=0,
)
```

Modèles disponibles :
- `gemini-2.5-flash` - Rapide et performant (recommandé)
- `gemini-2.5-pro` - Plus puissant mais plus lent
- `gemini-2.0-flash-lite` - Très rapide, moins précis

### Ajouter de nouveaux outils

1. Crée une fonction dans `agent/tools.py`
2. Décore-la avec `@tool`
3. Ajoute-la à la liste `TOOLS`

**Exemple :**

```python
@tool
def sort_data(column: str, ascending: bool = True) -> str:
    """
    Trie le DataFrame selon une colonne.

    Args:
        column: Colonne de tri
        ascending: True pour ordre croissant
    """
    df = get_dataframe()
    sorted_df = df.sort_values(by=column, ascending=ascending)
    return sorted_df.to_string()

# Ajoute à TOOLS
TOOLS = [
    get_head,
    get_info,
    calculate_stats,
    filter_data,
    group_by,
    sort_data,  # ← Nouveau tool
]
```

## 📊 Quotas API Gemini (version gratuite)

- **15 requêtes/minute**
- **20 requêtes/jour** (pour certains modèles)
- **Gratuit** pour une utilisation raisonnable

Si tu atteins le quota :
- Attends quelques minutes/heures
- Crée une nouvelle clé API
- Ou utilise un modèle local (Ollama)

## 🐛 Dépannage

### Erreur "Module not found"

```bash
# Réinstalle les dépendances
pip install -r requirements.txt
```

### Erreur "RESOURCE_EXHAUSTED" (quota dépassé)

1. Attends que le quota se réinitialise
2. Ou crée une nouvelle clé API sur [aistudio.google.com](https://aistudio.google.com)

### Le DataFrame ne se charge pas

Vérifie que :
- Le fichier CSV existe
- Le chemin est correct
- Le CSV est bien formaté (headers, virgules...)

## ⚠️ Limitations et évolutions futures

### Limitations actuelles

Ce projet est un **POC (Proof of Concept)** éducatif. Voici ses principales limitations :

#### 🔴 Architecture actuelle (Single-user, Stateless)

- **Pas de persistance** : L'historique des conversations est perdu au redémarrage
- **Pas de gestion multi-utilisateurs** : Un seul utilisateur à la fois
- **Pas d'authentification** : Pas de système de login/comptes utilisateurs
- **Pas de sessions** : Impossible de reprendre une conversation précédente
- **DataFrame en mémoire** : Variable globale, pas de gestion concurrente

#### 🟡 Autres limitations

- **Quotas API limités** : Version gratuite de Gemini (20 requêtes/jour selon le modèle)
- **Pas de cache** : Chaque question appelle l'API (même si déjà posée)
- **Tools limités** : Seulement 5 opérations pandas de base
- **Pas de visualisations** : Pas de graphiques (matplotlib/plotly)
- **Format unique** : Seulement CSV (pas Excel, JSON, SQL...)
- **Pas de validation robuste** : Gestion d'erreurs basique

### 🚀 Évolutions pour un projet production-ready

Pour transformer ce POC en application d'entreprise multi-utilisateurs, il faudrait :

#### 1. **Base de données et persistance**

```python
# Architecture cible
PostgreSQL/MongoDB
├── users (id, email, password_hash, created_at)
├── conversations (id, user_id, title, created_at)
├── messages (id, conversation_id, role, content, timestamp)
└── uploaded_files (id, user_id, filename, path, metadata)
```

**Technologies** : PostgreSQL + SQLAlchemy ou MongoDB + Motor (async)

#### 2. **Authentification et sessions**

```python
# Ajouts nécessaires
- JWT tokens pour l'authentification
- Session management avec Redis
- User profiles et permissions
- Rate limiting par utilisateur
```

**Technologies** : FastAPI + JWT + Redis

#### 3. **Architecture asynchrone scalable**

```python
# Architecture micro-services
┌─────────────────────────────────────┐
│  Frontend (Streamlit / React)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  API Gateway (FastAPI)               │
│  - Authentication                    │
│  - Rate limiting                     │
│  - Load balancing                    │
└──────────────┬───────────────────────┘
               │
        ┌──────┴───────┐
        ▼              ▼
┌─────────────┐  ┌─────────────┐
│  Agent      │  │  File       │
│  Service    │  │  Service    │
│  (async)    │  │  (async)    │
└─────┬───────┘  └──────┬──────┘
      │                 │
      ▼                 ▼
┌─────────────────────────────┐
│  PostgreSQL / MongoDB        │
│  Redis (cache + sessions)    │
└──────────────────────────────┘
```

**Technologies** : FastAPI (async) + Celery (workers) + PostgreSQL + Redis

#### 4. **Features avancées**

- **Multi-DataFrames** : Comparer plusieurs fichiers
- **Visualisations** : Intégration matplotlib/plotly
- **Export** : PDF, Excel, rapports automatiques
- **Cache intelligent** : Redis pour les réponses fréquentes
- **Monitoring** : Prometheus + Grafana pour les métriques
- **Logs structurés** : ELK stack (Elasticsearch, Logstash, Kibana)
- **CI/CD** : GitHub Actions + tests automatisés
- **Déploiement** : Kubernetes pour la scalabilité

#### 5. **Sécurité renforcée**

- [ ] Validation stricte des inputs (injection SQL, XSS)
- [ ] Chiffrement des données sensibles
- [ ] Audit logs pour traçabilité
- [ ] HTTPS obligatoire
- [ ] CORS configuré correctement
- [ ] Secrets management (Vault, AWS Secrets Manager)

### 📖 Ressources pour aller plus loin

**LangChain & LangGraph**
- [LangGraph Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
- [LangChain Production Best Practices](https://python.langchain.com/docs/guides/productionization/)

**Scalabilité**
- [FastAPI Async Patterns](https://fastapi.tiangolo.com/async/)
- [Celery Distributed Task Queue](https://docs.celeryq.dev/)

**Architecture**
- [Microservices avec Python](https://microservices.io/patterns/microservices.html)
- [The Twelve-Factor App](https://12factor.net/)

---

**En résumé** : Ce projet est une excellente base pour apprendre, mais nécessite des refactoring significatives (DB, auth, async workers, monitoring) pour supporter une utilisation multi-utilisateurs en production.

## 📚 Technologies utilisées

- **[LangChain](https://python.langchain.com/)** - Framework pour applications LLM
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Orchestration d'agents
- **[Google Gemini](https://ai.google.dev/)** - LLM de Google (via API)
- **[Pandas](https://pandas.pydata.org/)** - Analyse de données
- **[Streamlit](https://streamlit.io/)** - Interface web
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Gestion des variables d'environnement

## 📄 Licence

MIT License - Tu es libre d'utiliser, modifier et distribuer ce code.

## 👤 Auteur

Créé avec ❤️ pour apprendre LangChain et LangGraph

---

**Besoin d'aide ?** Ouvre une issue sur GitHub ou consulte la [documentation LangChain](https://python.langchain.com/).
