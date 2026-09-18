
# Backend - Engine API

This is the core engine of the application. It is a layered REST API built with [FastAPI](https://fastapi.tiangolo.com/), responsible for game logic, player management, and data persistence.

## 🚀 Run the application

Command to run from the repository's root directory:

- Install all dependencies: `uv sync --project backend --all-extras`
  - option all-extras: including dev dependancies
- Launch the API in development mode: `uv run --project backend python backend/src/main.py`

:bulb: First Launch: Click on **Reset Database** to initialize it.

## 🏛️ Architecture

The backend follows a **Layered Architecture** (N-Tier) to ensure separation of concerns and maintainability:

- **Business Object** (`business_object/`) : Represents the pure domain entities
- **Controller** (`controller/`) : Handles HTTP requests and routing via FastAPI
- **Service** (`service/`) : Contains the core business logic
- **DAO** (`dao/`) : Manages database interactions
- **API_OSV** (`api_osv/`) : Manages external api interactions
- **Schema** (`schema/`) : Data contract via [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/) to ensure API requests and responses follow a strict structure

### Layers

Sequence diagram of the player retrieval flow through the application layers:

```mermaid
%%{init: {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#f1f6ff",
        "primaryTextColor": "#1F2937",
        "primaryBorderColor": "#6B8FC4",
        "lineColor": "#4B5563",
        "secondaryColor": "#F3F4F6",
        "tertiaryColor": "#FFFFFF",
        "actorBkg": "#f1f6fe",
        "actorBorder": "#6B8FC4",
        "actorTextColor": "#1F2937",
        "actorLineColor": "#9CA3AF",
        "signalColor": "#4B5563",
        "signalTextColor": "#1F2937",
        "labelBoxBkgColor": "#F3F4F6",
        "labelBoxBorderColor": "#9CA3AF",
        "labelTextColor": "#1F2937",
        "noteBkgColor": "#E8F0FE",
        "noteBorderColor": "#688cc3",
        "noteTextColor": "#1F2937",
        "activationBkgColor": "#DCE6F7",
        "activationBorderColor": "#7c9ac8",
        "loopTextColor": "#1F2937",
        "altBackground": "#F8FAFC",
        "altBorderColor": "#9CA3AF",
        "sequenceNumberColor": "#1F2937"
    }
}}%%

sequenceDiagram
    actor Utilisateur
    participant API
    participant DAO
    participant BDD@{ "type" : "database" }

    rect rgb(225, 245, 255)
        Note over Utilisateur,BDD: Demander un audit

        Utilisateur-->>API: Demande un audit sur un projet
        API-->>DAO: Demande les fichiers du projet
        DAO-->>BDD: Demande les informations relatives au projet
        DAO-->>API: Envoie les informations liées au projet à auditer
        API-->>Utilisateur: Donne les résultats de l'audit
    end

    rect rgb(225, 245, 230)
        Note over Utilisateur,BDD: Importer un projet

        Utilisateur->>API: Dépose un projet<br/>(projet + clé HMAC)
        API->>API: Vérifie la clé HMAC

        alt Clé HMAC incorrecte
            API-->>Utilisateur: Erreur : Création refusée
        else Clé HMAC correcte
            API->>DAO: Transmet les informations du projet
            DAO->>BDD: Crée le projet
            DAO->>BDD: Crée le fichier de code
            DAO->>BDD: Crée le fichier de dépendances
            DAO-->>API: Projet créé avec ses fichiers
            API-->>Utilisateur: Confirmation de l'importation du Projet
        end
    end

    rect rgb(254, 239, 226)
        Note over Utilisateur,BDD: Création d'un user

        Utilisateur->>API: Dépose les informations relatives à l'utilisation
        API->>DAO: Vérifier si le nom existe
        DAO->>BDD: Demande les informations relatives au nom du user donné

        alt Nom déjà utilisé
            DAO-->>API: Nom existant
            API-->>Utilisateur: Erreur : Nom déjà utilisé
        else Nom disponible
            API->>API: Hasher le mot de passe
            API->>DAO: Créer l'utilisateur
            DAO->>BDD: Enregistre les informations de l'utilisateur
            DAO-->>API: Utilisateur créé
            API-->>Utilisateur: Confirmation de la création du compte
        end
    end
````

### Config files

In both the backend and frontend folders, you will find:

| Item                  | Description                                         | 
| --------------------- | --------------------------------------------------- | 
| logging_config.yml    | Configuration for the structured logging system.    | 
| pyproject.toml        | Project metadata and dependency definitions.        | 
| uv.lock               | Lockfile that ensures reproducible environments by pinning exact dependency versions. |
| \_\_init\_\_.py       | Marks a directory as a Python package, enabling module imports. |


## ⚒️ Development toolkit

### Debugging & Logs

The application uses a structured logging system. Logs are written to the `backend/logs/` directory and follow the format defined in `logging_config.yml`.

A custom `@log` decorator is available to automatically log method inputs and outputs, making it much easier to trace the flow of data through the services.

### Unit tests

To ensure tests are repeatable, safe, and **do not interfere with the real database**, we use a dedicated schema for unit testing.

The DAO unit tests use data from the `data/pop_db_test.sql` file.

This data is loaded into a separate schema (project_test_dao) so as not to pollute the other data.

- [ ] Lanch unit tests: `uv run --project backend pytest -v` 

It is also possible to generate test coverage using [Coverage](https://coverage.readthedocs.io/en/)

- [ ] `uv run --project backend coverage run -m pytest backend`
- [ ] `uv run --project backend coverage report -m`
- [ ] `uv run --project backend coverage html`
  - Download and open coverage_report/index.html

### Ruff

The **format on save** with [Ruff](https://docs.astral.sh/ruff/) is enabled by default in the workspace (cf. *.vscode/settings.json*).

To do it manually:

- ensures consistent and readable code style: `uv run --project backend ruff format backend/`
- identifies and fixes potential issues: `uv run --project frontend ruff check --fix backend/`


### Pylint

Static analysis with **pylint**: `uv run --project backend --extra dev pylint --output-format=colorized --disable=C0114,C0411,C0415,W0718 $(git ls-files 'backend/**/*.py') --fail-under=7.5`
