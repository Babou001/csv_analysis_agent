# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [v2.0.0] - Améliorations Production-Ready - 2025-03-22

### ✨ Nouvelles fonctionnalités

#### 1. Configuration externalisée
- **Prompts dans fichiers** : Le prompt système est maintenant dans `prompts/system.txt`
- **Configuration centralisée** : Nouveau fichier `agent/config.py` pour tous les paramètres
- **Plus maintenable** : Changements de prompts sans toucher au code

#### 2. Support asynchrone
- **Nouveau fichier** : `agent/graph_async.py` avec version async du graphe
- **Scalabilité** : Supporte plusieurs requêtes simultanées (async/await)
- **Performance** : Meilleure utilisation des ressources serveur
- **Base pour multi-utilisateurs** : Prépare le terrain pour une architecture scalable

#### 3. Docker et conteneurisation
- **Dockerfile** : Image Python 3.12 optimisée
- **docker-compose.yml** : Déploiement en un clic
- **Makefile** : Commandes simplifiées (`make up`, `make down`, etc.)
- **Portabilité** : Fonctionne de manière identique sur tous les OS
- **.dockerignore** : Optimisation de la taille d'image

#### 4. Documentation enrichie
- **Section limitations** : Limitations actuelles clairement documentées
- **Roadmap production** : Architecture cible pour multi-utilisateurs
- **Guide Docker** : Instructions complètes pour le déploiement
- **Note POC** : Clarification que c'est un projet éducatif

### 🔧 Améliorations techniques

- **Séparation des responsabilités** : Config séparée du code métier
- **Chargement dynamique** : Prompts chargés depuis fichiers
- **Non-root user** : Container Docker sécurisé
- **Best practices** : Architecture préparée pour évolution

### 📝 Documentation

- README.md enrichi avec :
  - Section Docker complète
  - Limitations et scope du projet
  - Architecture cible pour production
  - Roadmap détaillée (DB, auth, monitoring)
  - Technologies recommandées pour scale
- Nouveau fichier CHANGELOG.md
- Commentaires améliorés dans le code

### 🗂️ Structure du projet

Nouveaux fichiers :
```
├── agent/
│   ├── config.py           # ✨ Nouveau
│   └── graph_async.py      # ✨ Nouveau
├── prompts/
│   └── system.txt          # ✨ Nouveau
├── Dockerfile              # ✨ Nouveau
├── docker-compose.yml      # ✨ Nouveau
├── .dockerignore           # ✨ Nouveau
├── Makefile                # ✨ Nouveau
└── CHANGELOG.md            # ✨ Nouveau
```

### 🎯 Objectif de cette version

Transformer le POC initial en une base solide pour :
1. **Apprentissage** : Comprendre les bonnes pratiques
2. **Déploiement** : Docker-ready pour production
3. **Évolution** : Architecture préparée pour scaling
4. **Transparence** : Limitations clairement documentées

---

## [v1.0.0] - Version initiale - 2025-03-22

### 🎉 Fonctionnalités initiales

- 🧠 Agent LangGraph avec 5 tools pandas
- 💬 Interface CLI interactive
- 🌐 Interface web Streamlit
- 🔧 Outils pandas : get_head, get_info, calculate_stats, filter_data, group_by
- 📊 Analyse de fichiers CSV
- 🤖 Intégration Google Gemini
- 🔒 Gestion sécurisée des clés API (.env)

### 📚 Documentation

- README.md complet
- Exemples de questions
- Guide d'installation
- Structure du projet

### 🏗️ Architecture

- LangChain + LangGraph
- State management avec TypedDict
- Cycle agent → tools → agent
- System prompt intégré

---

## Format

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

### Types de changements

- `✨ Nouvelles fonctionnalités` - Ajout de fonctionnalités
- `🔧 Améliorations` - Changements dans le code existant
- `🐛 Corrections` - Corrections de bugs
- `📝 Documentation` - Changements dans la documentation
- `🔒 Sécurité` - Correctifs de sécurité
- `⚠️ Déprécié` - Fonctionnalités bientôt supprimées
- `🗑️ Supprimé` - Fonctionnalités supprimées
