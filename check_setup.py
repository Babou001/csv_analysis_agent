#!/usr/bin/env python3
"""
Script de vérification de l'installation.

Lance ce script pour vérifier que tout est correctement configuré.
Usage: python check_setup.py
"""

import sys
from pathlib import Path


def check_python_version():
    """Vérifie la version de Python"""
    print("🐍 Vérification de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (minimum requis: 3.8)")
        return False


def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    print("\n📦 Vérification des dépendances...")

    dependencies = [
        "langchain",
        "langchain_google_genai",
        "langgraph",
        "dotenv",
        "pandas",
        "streamlit",
    ]

    all_ok = True
    for dep in dependencies:
        try:
            if dep == "dotenv":
                __import__("dotenv")
                module_name = "python-dotenv"
            elif dep == "langchain_google_genai":
                __import__("langchain_google_genai")
                module_name = "langchain-google-genai"
            else:
                __import__(dep)
                module_name = dep

            print(f"   ✅ {module_name}")
        except ImportError:
            print(f"   ❌ {module_name} (exécute: pip install {module_name})")
            all_ok = False

    return all_ok


def check_env_file():
    """Vérifie que le fichier .env existe"""
    print("\n🔐 Vérification du fichier .env...")

    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ Fichier .env trouvé")

        # Vérifie que la clé API est présente
        content = env_file.read_text()
        if "GOOGLE_API_KEY=" in content and "ta_clé" not in content:
            print("   ✅ Clé API configurée")
            return True
        else:
            print("   ⚠️  Clé API non configurée (édite le fichier .env)")
            return False
    else:
        print("   ❌ Fichier .env manquant")
        print("      → Copie .env.example vers .env")
        print("      → Ajoute ta clé API Gemini")
        return False


def check_data_files():
    """Vérifie que les fichiers de données existent"""
    print("\n📂 Vérification des fichiers de données...")

    data_dir = Path("data")
    if not data_dir.exists():
        print("   ❌ Dossier data/ manquant")
        return False

    sample_file = data_dir / "ventes.csv"
    if sample_file.exists():
        print(f"   ✅ Fichier d'exemple présent ({sample_file})")
        return True
    else:
        print("   ⚠️  Fichier d'exemple manquant (optionnel)")
        return True


def check_project_structure():
    """Vérifie la structure du projet"""
    print("\n📁 Vérification de la structure...")

    required_files = [
        "agent/__init__.py",
        "agent/llm.py",
        "agent/tools.py",
        "agent/graph.py",
        "app_cli.py",
        "app_streamlit.py",
        "requirements.txt",
    ]

    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_ok = False

    return all_ok


def test_llm_connection():
    """Teste la connexion au LLM (optionnel)"""
    print("\n🤖 Test de connexion au LLM...")
    print("   ⏭️  Ignoré (pour préserver ton quota API)")
    print("   💡 Lance 'python agent/llm.py' pour tester manuellement")
    return True


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🔍 Vérification de l'installation - Agent DataFrame")
    print("=" * 60)

    checks = [
        ("Version Python", check_python_version()),
        ("Dépendances", check_dependencies()),
        ("Fichier .env", check_env_file()),
        ("Fichiers de données", check_data_files()),
        ("Structure du projet", check_project_structure()),
        ("Connexion LLM", test_llm_connection()),
    ]

    print("\n" + "=" * 60)
    print("📊 Résumé")
    print("=" * 60)

    all_passed = all(result for _, result in checks)

    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print("\n" + "=" * 60)

    if all_passed:
        print("✅ Tout est prêt ! Tu peux lancer l'application :")
        print("\n   Terminal:  python app_cli.py")
        print("   Web:       streamlit run app_streamlit.py")
    else:
        print("⚠️  Certaines vérifications ont échoué.")
        print("   Consulte les messages ci-dessus pour corriger.")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
