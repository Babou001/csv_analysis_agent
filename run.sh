#!/bin/bash

# Script utilitaire pour lancer les différentes commandes du projet
# Usage: ./run.sh [commande]

set -e  # Arrête en cas d'erreur

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction d'aide
show_help() {
    echo -e "${BLUE}📊 Agent DataFrame - Script utilitaire${NC}"
    echo ""
    echo "Usage: ./run.sh [commande]"
    echo ""
    echo "Commandes disponibles:"
    echo "  setup      - Installe les dépendances"
    echo "  check      - Vérifie l'installation"
    echo "  cli        - Lance l'interface terminal"
    echo "  web        - Lance l'interface Streamlit"
    echo "  test       - Teste l'agent"
    echo "  clean      - Nettoie les fichiers temporaires"
    echo ""
    echo "Exemples:"
    echo "  ./run.sh setup"
    echo "  ./run.sh cli"
}

# Fonction setup
setup() {
    echo -e "${BLUE}📦 Installation des dépendances...${NC}"

    # Vérifie si venv existe
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
        python3 -m venv venv
    fi

    # Active venv
    source venv/bin/activate

    # Installe les dépendances
    echo -e "${YELLOW}Installation des packages...${NC}"
    pip install -r requirements.txt

    echo -e "${GREEN}✅ Installation terminée !${NC}"
    echo ""
    echo "Prochaines étapes:"
    echo "  1. Copie .env.example vers .env"
    echo "  2. Ajoute ta clé API Gemini dans .env"
    echo "  3. Lance: ./run.sh check"
}

# Fonction check
check() {
    echo -e "${BLUE}🔍 Vérification de l'installation...${NC}"
    python check_setup.py
}

# Fonction cli
run_cli() {
    echo -e "${BLUE}🖥️  Lancement de l'interface CLI...${NC}"
    python app_cli.py
}

# Fonction web
run_web() {
    echo -e "${BLUE}🌐 Lancement de l'interface Streamlit...${NC}"
    streamlit run app_streamlit.py
}

# Fonction test
run_test() {
    echo -e "${BLUE}🧪 Tests de l'agent...${NC}"
    python test_cli.py
}

# Fonction clean
clean() {
    echo -e "${BLUE}🧹 Nettoyage...${NC}"

    # Supprime les fichiers Python compilés
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true

    # Supprime les fichiers temporaires
    rm -rf data/temp_* 2>/dev/null || true

    echo -e "${GREEN}✅ Nettoyage terminé !${NC}"
}

# Parse les arguments
case "$1" in
    setup)
        setup
        ;;
    check)
        check
        ;;
    cli)
        run_cli
        ;;
    web)
        run_web
        ;;
    test)
        run_test
        ;;
    clean)
        clean
        ;;
    *)
        show_help
        ;;
esac
