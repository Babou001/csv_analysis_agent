# Makefile pour Agent DataFrame
# Simplifie les commandes Docker et autres opérations

.PHONY: help build up down logs clean test check

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Affiche l'aide
	@echo "$(BLUE)📊 Agent DataFrame - Makefile$(NC)"
	@echo ""
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Construit l'image Docker
	@echo "$(BLUE)🔨 Construction de l'image Docker...$(NC)"
	docker-compose build

up: ## Lance les services Docker
	@echo "$(BLUE)🚀 Lancement des services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Streamlit disponible sur: http://localhost:8501$(NC)"

down: ## Arrête les services Docker
	@echo "$(BLUE)🛑 Arrêt des services...$(NC)"
	docker-compose down

logs: ## Affiche les logs
	docker-compose logs -f

restart: down up ## Redémarre les services

clean: ## Nettoie les fichiers temporaires et images Docker
	@echo "$(BLUE)🧹 Nettoyage...$(NC)"
	docker-compose down -v
	docker system prune -f
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

test: ## Lance les tests (sans appel LLM)
	@echo "$(BLUE)🧪 Tests...$(NC)"
	python check_setup.py

check: test ## Alias pour test

shell: ## Ouvre un shell dans le container
	docker-compose exec agent-dataframe /bin/bash

install: ## Installe les dépendances localement
	@echo "$(BLUE)📦 Installation des dépendances...$(NC)"
	pip install -r requirements.txt

run-local: ## Lance Streamlit en local (sans Docker)
	@echo "$(BLUE)🌐 Lancement de Streamlit en local...$(NC)"
	streamlit run app_streamlit.py

cli-local: ## Lance l'interface CLI en local (sans Docker)
	@echo "$(BLUE)🖥️  Lancement de l'interface CLI...$(NC)"
	python app_cli.py
