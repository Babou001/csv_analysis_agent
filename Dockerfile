# Dockerfile pour Agent DataFrame
# Image légère avec Python 3.12

FROM python:3.12-slim

# Métadonnées
LABEL maintainer="Agent DataFrame"
LABEL description="Agent d'analyse de données avec LangChain et LangGraph"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY agent/ ./agent/
COPY prompts/ ./prompts/
COPY data/ ./data/
COPY app_cli.py .
COPY app_streamlit.py .
COPY check_setup.py .

# Crée un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 agent && \
    chown -R agent:agent /app

USER agent

# Expose le port pour Streamlit
EXPOSE 8501

# Commande par défaut : interface Streamlit
CMD ["streamlit", "run", "app_streamlit.py", "--server.address", "0.0.0.0"]
