# ProjetFoot #

**État du projet :** En développement actif.

Ce projet vise à créer une plateforme pour explorer les ligues, joueurs et matchs, avec discussions contextuelles et gestion des rôles.

## Technologies utilisées ##
**Backend(En cours)** : Python, FastAPI, SQLAlchemy (ORM), PostgreSQL

**Frontend(En cours)** : Angular, TypeScript

**Authentification** : JWT (JSON Web Tokens)

**Test(Dans le futur)** : pytest

**Outils** : Git, pgAdmin

## Architecture du projet ##

Le backend suit une architecture propre pour séparer les responsabilités :

**app/constants/** : Constants cote backend.

**app/core/** : Logique de sécurité et d'authentification (JWT, hashing, contrôle d'accès par rôle).

**app/routers/** : Endpoints de l'API.

**app/crud/** : Logique de manipulation des données.

**app/models/** : Tables SQLAlchemy (base de données).

**app/schemas/** : Schémas Pydantic (validation des données).

**app/services/** : Services cote backend.

Le frontend suit :

**app/constants/** : Constants cote frontend.

**app/interfaces/** : Interfaces cote frontend.

**app/pages/** : Differentes pages.

**app/services/** : Services frontend.

**app/utils/** : Fonctions utilitaires.

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

    API_FOOTBALL_DATA_KEY=...

    API_FOOTBALL_DATA_KEY est donne dans https://www.api-football.com/.
    
6.  Lancer le serveur :

    uvicorn app.main:app --reload

7. Aller dans frontend/src/app:
    npm start
