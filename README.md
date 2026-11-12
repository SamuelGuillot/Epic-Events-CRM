# Epic Events CRM

Application en ligne de commande pour la gestion de la relation client d'Epic Events. Permet de gérer les collaborateurs, clients, contrats et événements.

## Fonctionnalités

- **Authentification** : inscription, connexion (JWT), déconnexion
- **Collaborateurs** : consultation, mise à jour (gestion)
- **Clients** : création et mise à jour (commercial)
- **Contrats** : création, mise à jour, signature (gestion)
- **Événements** : création (commercial, contrat signé), mise à jour (support), assignation d'un support (gestion)
- **Permissions** : chaque département a ses propres droits
- **Journalisation** : Sentry (erreurs, création/modification user, signature de contrat)
- **Menu interactif** : navigation par flèches (Questionary + Rich)

## Prérequis

- Python 3.12+
- Poetry : https://python-poetry.org/docs/#installation

## Installation

git clone https://github.com/SamuelGuillot/epic-events-crm.git
cd epic-events-crm
poetry install

## Configuration

Copiez `.env.example` en `.env` et renseignez les valeurs :

cp .env.example .env

Contenu du fichier `.env` :

JWT_SECRET_KEY=votre_cle_secrete_de_32_caracteres_minimum
JWT_EXPIRATION_HOURS=24
SENTRY_DSN=

## Base de données

Appliquer les migrations :

poetry run alembic upgrade head

## Utilisation

### Menu interactif

poetry run python run.py menu

### Commandes directes

Authentification :

poetry run python run.py register
poetry run python run.py login
poetry run python run.py logout

Clients :

poetry run python run.py client-list
poetry run python run.py client-create
poetry run python run.py client-update

Contrats :

poetry run python run.py contract-list
poetry run python run.py contract-create
poetry run python run.py contract-update --sign

Événements :

poetry run python run.py event-list
poetry run python run.py event-create
poetry run python run.py event-update

Aide générale :

poetry run python run.py --help

## Tests

poetry run pytest

## Qualité du code

poetry run black src/ tests/ run.py
poetry run isort src/ tests/ run.py
poetry run flake8

## Architecture

Le projet suit une architecture en couches :

CLI (src/cli/)                 -> Commandes, prompts, affichage
Service (src/services/)        -> Logique métier, permissions
Repository (src/repositories/) -> Requêtes SQL (SQLAlchemy)
Modèle (src/models/)           -> Tables et relations

- **DTO** (`src/DTO/`) : transportent les données entre les couches.
- **Permissions** (`src/permissions/`) : règles d'accès par département.
- **Exceptions** (`src/exceptions.py`) : erreurs typées, traduites par `src/cli/displays/error_display.py`.

### Arborescence

epic-events-crm/
├── run.py                  # Point d'entrée
├── alembic.ini             # Config Alembic
├── migrations/             # Migrations BDD
├── pyproject.toml          # Dépendances (Poetry)
├── .env                    # Secrets (non commité)
├── .env.example            # Modèle
├── src/
│   ├── cli/                # Présentation (Typer, Rich, Questionary)
│   │   ├── commands/       # Commandes par entité
│   │   └── displays/       # Affichages
│   ├── config/             # Base de données + Sentry
│   ├── DTO/                # Objets de transfert (dataclasses)
│   ├── models/             # Modèles SQLAlchemy
│   ├── permissions/        # Règles d'autorisation
│   ├── repositories/       # Accès aux données
│   └── services/           # Logique métier
└── tests/                  # Tests pytest

## Rôles et permissions

| Département  | Peut faire                                                     |
|--------------|----------------------------------------------------------------|
| Gestion      | CRUD collaborateurs, créer/modifier/signer tous les contrats, assigner un support, filtrer événements sans support |
| Commercial   | Créer/modifier ses clients, modifier contrats de ses clients, créer événements (contrat signé), filtrer contrats non signés |
| Support      | Modifier ses événements, filtrer ses propres événements |

Tous les collaborateurs peuvent consulter clients, contrats et événements en lecture seule.

## Stack technique

- Python 3.12 + Poetry
- Typer : structure des commandes CLI
- Rich + Questionary : affichage et menus interactifs
- SQLAlchemy : ORM
- Alembic : migrations
- SQLite : base de données (dev)
- PyJWT : authentification
- Argon2 : hachage des mots de passe
- Sentry : journalisation
- pytest : tests
- black / isort / flake8 : qualité du code