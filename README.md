# ProjetFoot #

**État du projet :** En développement actif (Backend en cours, Frontend prévu).

Ce projet vise à créer une plateforme de gestion de ligues sportives complète. Actuellement, l'accent est mis sur la solidité de l'API REST et la modélisation des données.

## Technologies utilisées ##
**Backend(En cours)** : Python, FastAPI, SQLAlchemy (ORM), PostgreSQL

**Frontend(Dans le futur)** : Angular, TypeScript

**Authentification** : JWT (JSON Web Tokens)

**Test(Dans le futur)** : pytest

**Outils** : Git, pgAdmin

## Architecture du projet ##

Le backend suit une architecture propre pour séparer les responsabilités :

**app/routers/** : Endpoints de l'API.

**app/crud/** : Logique de manipulation des données.

**app/models/** : Schémas SQLAlchemy (base de données).

**app/schemas/** : Schémas Pydantic (validation des données).

## Fonctionnalités principales

**Gestion complète (CRUD)** : Équipes, joueurs, entraîneurs, arbitres et stades.

**Sécurité** : Authentification sécurisée des utilisateurs et gestion des droits d'accès.

**Documentation** : API documentée automatiquement via Swagger UI (accessible sur /docs).

## Installation et exécution
**Prérequis** : Python 3.10+

**PostgreSQL** installé et configuré

**Étapes :**

1.  Cloner le dépôt :

    git clone https://github.com/haopchtat5693/ProjetFoot.git
    
    cd ProjetFoot


2.  Configuration de l'environnement :

    Créer le dossier venv : python -m venv venv
    
    Activer l'environnement :
    
    Sur Windows : venv\Scripts\activate
    
    Sur macOS/Linux : source venv/bin/activate
    
3.  Installer les dépendances :

    pip install -r requirements.txt
    
4.  Configurer les variables d'environnement :

    Créer un fichier .env à la racine

    Ajouter la configuration :
    
    DATABASE_URL=postgresql://votre_utilisateur:votre_mot_de_passe@localhost:5432/nom_de_votre_base
    
    SECRET_KEY=votre_cle_secrete
    
5.  Lancer le serveur :

    uvicorn app.main:app --reload

    Une fois le serveur lancé, accédez à la documentation interactive sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
