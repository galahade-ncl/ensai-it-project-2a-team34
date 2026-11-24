# Backend – Engine API

The backend is the core engine of the application. It is a layered REST API built with [FastAPI](https://fastapi.tiangolo.com/), responsible for the application's business logic, data processing and persistence.

This document explains how to configure, install and run the backend locally, as well as how to interact with its API.

# 🚀 Getting Started

## Installation and Configuration

### 1. Prerequisites

Before running the backend, make sure the following tools and services are available:

- Python
- `uv`
- An accessible PostgreSQL service
- Git

### 2. PostgreSQL Configuration

The backend uses an existing PostgreSQL service. You do not need to manually create the application's tables: they are initialized by the `reset_database` script.

Before proceeding, make sure that:
- The PostgreSQL service is running.
- You have the required connection credentials.
- The backend can connect to the PostgreSQL service.

### 3. Environment Variables

Create a `.env` file in the location expected by the backend, using `.env.example` as a reference if available.

Configure the required environment variables:

```env
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_DATABASE=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_SCHEMA=project

UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000

BACKEND_URL=http://localhost:5000
BACKEND_TIMEOUT=5

PASSWORD_MIN_LENGTH=16

CERT_SIGNING_PRIVATE_KEY=...
```

The values must match your PostgreSQL service configuration and backend settings.

**Important:** The `.env` file contains sensitive information and must never be committed to the Git repository.

### 4. Generate the Certificate Signing Key

The backend uses an Ed25519 key pair to sign certificates.

A script is provided to generate a new key pair. Run the script from a terminal:

```bash
uv run --project backend python backend/src/utils/generate_signing_key.py
```

The script prints the `CERT_SIGNING_PRIVATE_KEY` environment variable containing the private key in PEM format, with line breaks escaped.

Copy the generated value into your `.env` file.

**Important:** Keep the private key secure. The same private key should be retained for a given environment so that previously signed certificates can still be verified using the corresponding public key.

### 5. Install Dependencies

From the project root directory, install the backend dependencies:

```bash
uv sync --project backend --all-extras
```

### 6. Initialize the PostgreSQL Schema

**This step must only be performed when setting up the application for the first time.**

Run the `reset_database` script to initialize the PostgreSQL schema:

```bash
uv run --project backend python backend/src/utils/reset_database.py
```

The script performs the following operations:

1. Drops the schema specified by `POSTGRES_SCHEMA`, if it already exists.
2. Recreates the schema.
3. Creates the application tables using `data/init_db.sql`.
4. Inserts the initial data using `data/pop_db.sql`.
5. Updates the passwords of all existing users.

<blockquote>
  **Warning: This operation is destructive.**

  The script drops and recreates the entire configured schema. All existing data within that schema will be deleted, including users, projects and audit records.

  Do not run this script every time you start the backend. It should only be used for the initial database setup or when an intentional database reset is required.
</blockquote>

If the database schema has already been initialized, skip this step.

### 7. Start the Backend

Start the API using:

```bash
uv run --project backend python backend/src/main.py
```

The host and port depend on the values configured in `UVICORN_HOST` and `UVICORN_PORT`.

---

# 📚 API Documentation

This section describes the available API endpoints, their purpose, required parameters, request bodies, responses and possible errors.

The API is organized into six categories:

- **Users:** User account management.
- **Authentication:** User authentication and access token generation.
- **Projects:** Project creation and management.
- **Audits:** Audit execution and result retrieval.
- **HMAC Signatures:** HMAC signature generation.
- **Certificates:** Public key retrieval and certificate verification.

## 1. Endpoint Overview

| Category | Method | Endpoint | Description |
|---|---|---|---|
| Users | POST | `/user/` | Creates a new user account. |
| Users | PUT | `/user/{id_user}` | Updates the authenticated user's information. |
| Users | DELETE | `/user/{id_user}` | Deletes the authenticated user and their projects. |
| Users | GET | `/user/{id_user}/project` | Retrieves the authenticated user's projects. |
| Authentication | POST | `/login/` | Authenticates a user and returns an access token. |
| Projects | POST | `/project/` | Creates a project and generates its HMAC secret key. |
| Projects | GET | `/project/{id_project}` | Retrieves project information. |
| Projects | PUT | `/project/{id_project}` | Updates an existing project. |
| Projects | DELETE | `/project/{id_project}` | Deletes a project. |
| Projects | POST | `/project/{id_project}/secret-key` | Generates a new HMAC secret key for a project. |
| Projects | GET | `/project/{id_project}/audit` | Retrieves the audits associated with a project. |
| Audits | POST | `/audit/` | Runs an audit after verifying the HMAC signature. |
| Audits | GET | `/audit/{id_audit}` | Retrieves audit information. |
| Audits | GET | `/audit/{id_audit}/certificate` | Downloads the PDF certificate of an audit. |
| Audits | GET | `/audit/{id_audit}/sbom` | Downloads the SBOM of an audit. |
| HMAC Signatures | POST | `/hmac/signature` | Generates an HMAC signature for the submitted project files. |
| Certificates | GET | `/.well-known/public-key` | Exposes the public key used to sign certificates. |
| Certificates | POST | `/certificate/verify` | Verifies the signature of a certificate. |

````mermaid
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
    participant BDD@{ "type": "database" }

    rect rgb(225, 245, 255)
    Note over Utilisateur,BDD: Créer un utilisateur
    Utilisateur->>API: POST /user/<br/>Dépose les informations de l'utilisateur
    API->>DAO: Vérifier si le nom existe
    DAO->>BDD: Recherche un utilisateur par le username
    BDD-->>DAO: Résultat de la recherche
    alt Nom déjà utilisé
        DAO-->>API: Nom existant
        API-->>Utilisateur: Erreur : nom déjà utilisé
    else Nom disponible
        DAO-->>API: Nom disponible
        API->>API: Hashe le mot de passe
        API->>DAO: Crée l'utilisateur
        DAO->>BDD: Enregistre les informations de l'utilisateur
        BDD-->>DAO: Utilisateur enregistré
        DAO-->>API: Utilisateur créé
        API-->>Utilisateur: Confirmation de la création du compte
    end
    end

    rect rgb(254, 239, 226)
    Note over Utilisateur,BDD: Modifier un utilisateur
    Utilisateur->>API: PUT /user/{id_user}<br/>Envoie les nouvelles informations
    API->>DAO: Met à jour l'utilisateur
    DAO->>BDD: Enregistre les modifications
    BDD-->>DAO: Utilisateur modifié
    DAO-->>API: Utilisateur modifié
    API-->>Utilisateur: Confirmation de la modification du compte
    end

    rect rgb(254, 238, 255)
    Note over Utilisateur,BDD: Supprimer un utilisateur
    Utilisateur->>API: DELETE /user/{id_user}<br/>Demande la suppression du compte
    API->>DAO: Supprime l'utilisateur
    DAO->>BDD: Supprime l'utilisateur
    BDD-->>DAO: Utilisateur supprimé
    DAO-->>API: Utilisateur supprimé
    API-->>Utilisateur: Confirmation de la suppression du compte
    end

    rect rgb(225, 245, 255)
    Note over Utilisateur,BDD: Lister les projets d'un utilisateur
    Utilisateur->>API: GET /user/{id_user}/project<br/>Demande ses projets
    API->>DAO: Demande les projets de l'utilisateur
    DAO->>BDD: Recherche les projets de l'utilisateur
    BDD-->>DAO: Liste des projets
    DAO-->>API: Liste des projets
    API-->>Utilisateur: Liste des projets de l'utilisateur
    end

    rect rgb(225, 245, 230)
    Note over Utilisateur,BDD: Se connecter
    Utilisateur->>API: POST /login/<br/>Envoie ses identifiants (username, password)
    API->>DAO: Demande l'utilisateur
    DAO->>BDD: Recherche l'utilisateur par le username
    BDD-->>DAO: Utilisateur et mot de passe hashé
    DAO-->>API: Utilisateur
    API->>API: Vérifie le mot de passe
    alt Identifiants incorrects
        API-->>Utilisateur: Erreur : identifiants incorrects
    else Identifiants valides
        API-->>Utilisateur: Jeton d'accès (token)
    end
    end

    rect rgb(225, 245, 230)
    Note over Utilisateur,BDD: Importer un projet
    Utilisateur->>API: POST /project/<br/>Dépose un projet
    API->>API: Génère la clé secrète HMAC du projet
    API->>DAO: Crée le projet
    DAO->>BDD: Enregistre le projet et sa clé
    BDD-->>DAO: Projet enregistré
    DAO-->>API: Projet créé
    API-->>Utilisateur: Confirmation de l'importation du projet<br/>+ renvoie la clé secrète HMAC
    end

    rect rgb(254, 239, 226)
    Note over Utilisateur,BDD: Consulter un projet
    Utilisateur->>API: GET /project/{id_project}<br/>Demande les informations du projet
    API->>DAO: Demande le projet
    DAO->>BDD: Recherche le projet
    BDD-->>DAO: Informations du projet
    DAO-->>API: Informations du projet
    API-->>Utilisateur: Informations du projet
    end

    rect rgb(254, 238, 255)
    Note over Utilisateur,BDD: Modifier un projet
    Utilisateur->>API: PUT /project/{id_project}<br/>Envoie les nouvelles informations
    API->>DAO: Met à jour le projet
    DAO->>BDD: Enregistre les modifications
    BDD-->>DAO: Projet modifié
    DAO-->>API: Projet modifié
    API-->>Utilisateur: Confirmation de la modification du projet
    end

    rect rgb(225, 245, 255)
    Note over Utilisateur,BDD: Supprimer un projet
    Utilisateur->>API: DELETE /project/{id_project}<br/>Demande la suppression du projet
    API->>DAO: Supprime le projet
    DAO->>BDD: Supprime le projet
    BDD-->>DAO: Projet supprimé
    DAO-->>API: Projet supprimé
    API-->>Utilisateur: Confirmation de la suppression du projet
    end

    rect rgb(225, 245, 230)
    Note over Utilisateur,BDD: Lister les audits d'un projet
    Utilisateur->>API: GET /project/{id_project}/audit<br/>Demande les audits du projet
    API->>DAO: Demande les audits du projet
    DAO->>BDD: Recherche les audits du projet
    BDD-->>DAO: Liste des audits
    DAO-->>API: Liste des audits
    API-->>Utilisateur: Liste des audits du projet
    end

    rect rgb(254, 239, 226)
    Note over Utilisateur,BDD: Demander une signature HMAC
    Utilisateur->>API: POST /hmac/signature<br/>Envoie le code et le fichier de dépendances<br/>+ clé secrète HMAC
    API->>API: Génère la signature HMAC
    API-->>Utilisateur: Renvoie la signature
    end

    rect rgb(254, 238, 255)
    Note over Utilisateur,BDD: Demander un audit
    Utilisateur->>API: POST /audit/<br/>Envoie le code et le fichier de dépendances<br/>+ signature HMAC
    API->>DAO: Demande le projet et sa clé secrète
    DAO->>BDD: Recherche le projet
    BDD-->>DAO: Informations et clé secrète
    DAO-->>API: Informations et clé secrète
    API->>API: Vérifie la signature HMAC
    alt Signature incorrecte
        API-->>Utilisateur: Erreur : signature incorrecte
    else Signature correcte
        API->>API: Réalise l'audit (analyse du code,<br/>API deps.dev, API OSV)
        API->>API: Génère le SBOM et le certificat signé (Ed25519)
        API->>DAO: Enregistre les résultats de l'audit
        DAO->>BDD: Enregistre audit, SBOM et certificat
        BDD-->>DAO: Audit enregistré
        DAO-->>API: Audit créé
        API-->>Utilisateur: Renvoie les résultats de l'audit
    end
    end

    rect rgb(225, 245, 255)
    Note over Utilisateur,BDD: Consulter les résultats d'un audit
    Utilisateur->>API: GET /audit/{id_audit}<br/>Demande les résultats de l'audit
    API->>DAO: Demande l'audit
    DAO->>BDD: Recherche l'audit
    BDD-->>DAO: Résultats de l'audit
    DAO-->>API: Résultats de l'audit
    API-->>Utilisateur: Résultats de l'audit
    end

    rect rgb(225, 245, 230)
    Note over Utilisateur,BDD: Télécharger le certificat PDF
    Utilisateur->>API: GET /audit/{id_audit}/certificate<br/>Demande le certificat
    API->>DAO: Demande le certificat de l'audit
    DAO->>BDD: Recherche le certificat
    BDD-->>DAO: Certificat PDF
    DAO-->>API: Certificat PDF
    API-->>Utilisateur: Certificat PDF
    end

    rect rgb(254, 239, 226)
    Note over Utilisateur,BDD: Télécharger le SBOM
    Utilisateur->>API: GET /audit/{id_audit}/sbom<br/>Demande le SBOM
    API->>DAO: Demande le SBOM de l'audit
    DAO->>BDD: Recherche le SBOM
    BDD-->>DAO: SBOM
    DAO-->>API: SBOM
    API-->>Utilisateur: SBOM
    end

    rect rgb(254, 238, 255)
    Note over Utilisateur,BDD: Récupérer la clé publique
    Utilisateur->>API: GET /.well-known/public-key
    API-->>Utilisateur: Clé publique, identifiant, algorithme de signature Ed25519
    end

    rect rgb(225, 245, 255)
    Note over Utilisateur,BDD: Vérifier un certificat
    Utilisateur->>API: POST /certificate/verify<br/>Envoie le certificat
    API->>API: Vérifie la signature et la validité
    API-->>Utilisateur: Certificat authentique ou invalide
    end

````

## 2. Authentication

Most API endpoints require authentication through an access token.

To obtain a token, the user must first authenticate using `POST /login/`.

The token must then be included in the `Authorization` header of protected requests:

```http
Authorization: Bearer <access_token>
```

The following endpoints do not require an authentication token:

- `POST /user/`
- `POST /login/`
- `GET /.well-known/public-key`
- `POST /certificate/verify`

All other endpoints documented below use the `verify_token` dependency.

## 3. User Management

### 3.1. Create a User

**Method:** `POST`

**Route:** `/user/`

**Authentication:** Not required.

**Purpose:**

Creates a new user account.

**Request body:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | String | Yes | Username of the new user. |
| `password` | String | Yes | Password of the new user. |
| `email` | String | Yes | Email address of the new user. |

The exact validation constraints are defined in `UserModel`.

**Expected response:**

`UserReadModel` containing the newly created user information.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | User successfully created. |
| 400 | Username already exists. |
| 500 | Error while creating the user. |
| 422 | Request validation error. |

### 3.2. Update a User

**Method:** `PUT`

**Route:** `/user/{id_user}`

**Authentication:** Required.

**Purpose:**

Updates the username, password and email address of the authenticated user.

**Request body:**

`UserResponseModel`.

The expected fields are:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | String | Yes | New username. |
| `password` | String | Yes | New password. |
| `email` | String | Yes | New email address. |

**Expected response:**

`UserReadModel` containing the updated user information.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | User successfully updated. |
| 400 | Username already exists. |
| 500 | Error while updating the user. |
| 422 | Request validation error. |

**Note:** The current implementation uses the authenticated user's ID rather than the `id_user` value from the URL.

### 3.3. Delete a User

**Method:** `DELETE`

**Route:** `/user/{id_user}`

**Authentication:** Required.

**Purpose:**

Deletes the authenticated user and all projects associated with that user.

**Request parameters:**

No request body is required.

**Expected response:**

A confirmation message:

```text
User <username> deleted
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | User successfully deleted. |
| 404 | User not found. |

**Note:** The current implementation deletes the authenticated user, not the user identified by the URL parameter.

### 3.4. Retrieve a User's Projects

**Method:** `GET`

**Route:** `/user/{id_user}/project`

**Authentication:** Required.

**Purpose:**

Retrieves all projects belonging to the authenticated user.

**Expected response:**

A list of `ProjectReadModel` objects.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Projects successfully retrieved. |
| 422 | Request validation error. |

**Note:** The current implementation uses the authenticated user's ID rather than the `id_user` value from the URL.

## 4. Authentication

### 4.1. Login

**Method:** `POST`

**Route:** `/login/`

**Authentication:** Not required.

**Purpose:**

Authenticates a user using their username and password and returns an access token.

**Request body:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | String | Yes | User's username. |
| `password` | String | Yes | User's password. |

**Example request:**

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

**Expected response:**

```json
{
  "id_user": 1,
  "username": "example_user",
  "access_token": "<access_token>"
}
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Authentication successful. |
| 401 | Invalid credentials. |
| 422 | Request validation error. |

## 5. Project Management

### 5.1. Create a Project

**Method:** `POST`

**Route:** `/project/`

**Authentication:** Required.

**Purpose:**

Creates a new project associated with the authenticated user and generates a secret HMAC key.

**Request body:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name_project` | String | Yes | Name of the project. |

**Example request:**

```json
{
  "name_project": "My Project"
}
```

**Expected response:**

`ProjectResponseModel` containing:

- `id_project`: Project identifier.
- `name_project`: Project name.
- `secretHMACkey`: HMAC secret key encoded in Base64.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Project successfully created. |
| 500 | Error while creating the project. |
| 422 | Request validation error. |

### 5.2. Retrieve a Project

**Method:** `GET`

**Route:** `/project/{id_project}`

**Authentication:** Required.

**Purpose:**

Retrieves information about a project owned by the authenticated user.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_project` | Integer | Yes | Unique project identifier. |

**Expected response:**

`ProjectReadModel` containing the project information.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Project successfully retrieved. |
| 404 | Project not found or access denied. |
| 422 | Invalid project identifier. |

### 5.3. Update a Project

**Method:** `PUT`

**Route:** `/project/{id_project}`

**Authentication:** Required.

**Purpose:**

Updates the name of an existing project owned by the authenticated user.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_project` | Integer | Yes | Unique project identifier. |

**Request body:**

`ProjectCreateModel`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name_project` | String | Yes | New project name. |

**Example request:**

```json
{
  "name_project": "Updated Project Name"
}
```

**Expected response:**

`ProjectReadModel` containing the updated project information.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Project successfully updated. |
| 404 | Project not found or access denied. |
| 500 | Error while updating the project. |
| 422 | Request validation error. |

### 5.4. Delete a Project

**Method:** `DELETE`

**Route:** `/project/{id_project}`

**Authentication:** Required.

**Purpose:**

Deletes a project owned by the authenticated user.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_project` | Integer | Yes | Unique project identifier. |

**Expected response:**

A confirmation message:

```text
Project <project_name> deleted
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Project successfully deleted. |
| 404 | Project not found or access denied. |
| 422 | Invalid project identifier. |

### 5.5. Regenerate a Project Secret Key

**Method:** `POST`

**Route:** `/project/{id_project}/secret-key`

**Authentication:** Required.

**Purpose:**

Generates a new HMAC secret key for an existing project.

The previous secret key is no longer valid after regeneration.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_project` | Integer | Yes | Unique project identifier. |

**Request body:**

None.

**Expected response:**

```json
{
  "id_project": 1,
  "name_project": "My Project",
  "secretHMACkey": "<base64_encoded_secret_key>"
}
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Secret key successfully regenerated. |
| 404 | Project not found or access denied. |
| 500 | Could not regenerate the secret key. |

### 5.6. Retrieve a Project's Audits

**Method:** `GET`

**Route:** `/project/{id_project}/audit`

**Authentication:** Required.

**Purpose:**

Retrieves all audits associated with a project owned by the authenticated user.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_project` | Integer | Yes | Unique project identifier. |

**Expected response:**

A list of `AuditReadModel` objects.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Audits successfully retrieved. |
| 404 | Project not found or access denied. |
| 422 | Invalid project identifier. |

## 6. Audit Management

### 6.1. Create an Audit

**Method:** `POST`

**Route:** `/audit/`

**Authentication:** Required.

**Purpose:**

Runs a complete audit on a project.

The endpoint:
1. Checks that the project belongs to the authenticated user.
2. Decodes the submitted code and dependency files from Base64.
3. Decodes and verifies the HMAC signature.
4. Runs the audit.
5. Returns the audit results, including the certificate and SBOM when available.

**Request body:**

`AuditCreateModel`.

The following fields are accessed by the controller:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `project.id_project` | Integer | Yes | Identifier of the project to audit. |
| `project.codefile.name` | String | Yes | Name of the source code file. |
| `project.codefile.content` | String | Yes | Source code content encoded in Base64. |
| `project.codefile.type_file` | String | Yes | Source code file type. |
| `project.dependencyfile.name` | String | Yes | Name of the dependency file. |
| `project.dependencyfile.content` | String | Yes | Dependency file content encoded in Base64. |
| `project.dependencyfile.type_file` | String | Yes | Dependency file type. |
| `qualitygate_type` | String | Yes | Quality gate configuration used for the audit. |
| `hmac_signature` | String | Yes | HMAC signature encoded in Base64. |

**Example request structure:**

```json
{
  "project": {
    "id_project": 1,
    "codefile": {
      "name": "main.py",
      "content": "<base64_encoded_code>",
      "type_file": "python"
    },
    "dependencyfile": {
      "name": "requirements.txt",
      "content": "<base64_encoded_dependencies>",
      "type_file": "requirements"
    }
  },
  "qualitygate_type": "<quality_gate_type>",
  "hmac_signature": "<base64_encoded_signature>"
}
```

The example illustrates the structure only. The exact accepted values for `type_file` and `qualitygate_type` must be checked in the corresponding models and services.

**Expected response:**

`AuditResponseModel` containing the newly created audit information.

The binary certificate and SBOM contents are Base64-encoded before being returned when available.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Audit successfully created. |
| 400 | Invalid Base64 content in files or signature. |
| 401 | Invalid HMAC signature. |
| 404 | Project not found or access denied. |
| 500 | Error while creating the audit. |
| 422 | Request validation error. |

### 6.2. Retrieve an Audit

**Method:** `GET`

**Route:** `/audit/{id_audit}`

**Authentication:** Required.

**Purpose:**

Retrieves the results and information of an audit, provided that the authenticated user owns the associated project.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_audit` | Integer | Yes | Unique audit identifier. |

**Expected response:**

`AuditReadModel` containing the audit information.

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Audit successfully retrieved. |
| 404 | Audit not found or access denied. |
| 422 | Invalid audit identifier. |

### 6.3. Download an Audit Certificate

**Method:** `GET`

**Route:** `/audit/{id_audit}/certificate`

**Authentication:** Required.

**Purpose:**

Downloads the PDF certificate generated after an audit.

The authenticated user must own the project associated with the audit.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_audit` | Integer | Yes | Unique audit identifier. |

**Expected response:**

A PDF file returned as an attachment.

Example filename:

```text
certificate_1.pdf
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Certificate successfully downloaded. |
| 404 | Audit not found, access denied or certificate unavailable. |
| 500 | Invalid certificate content. |
| 422 | Invalid audit identifier. |

### 6.4. Download an Audit SBOM

**Method:** `GET`

**Route:** `/audit/{id_audit}/sbom`

**Authentication:** Required.

**Purpose:**

Downloads the Software Bill of Materials (SBOM) generated during an audit.

The authenticated user must own the project associated with the audit.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id_audit` | Integer | Yes | Unique audit identifier. |

**Expected response:**

A JSON file returned as an attachment.

Example filename:

```text
sbom_1.json
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | SBOM successfully downloaded. |
| 404 | Audit not found, access denied or SBOM unavailable. |
| 422 | Invalid audit identifier. |

## 7. HMAC Signature Generation

### 7.1. Generate an HMAC Signature

**Method:** `POST`

**Route:** `/hmac/signature`

**Authentication:** Required.

**Purpose:**

Generates an HMAC signature for a project's source code and dependency files.

The signature is computed using:
- The project's secret HMAC key.
- The project identifier.
- The source code file content.
- The dependency file content.

The generated signature can then be included in the `POST /audit/` request.

**Request body:**

`HmacSignatureRequest`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `secret` | String | Yes | Project HMAC secret key encoded in Base64. |
| `project_id` | Integer | Yes | Unique project identifier. |
| `code` | String | Yes | Source code content encoded in Base64. |
| `dependency` | String | Yes | Dependency file content encoded in Base64. |

**Example request:**

```json
{
  "secret": "<base64_encoded_secret_key>",
  "project_id": 1,
  "code": "<base64_encoded_code>",
  "dependency": "<base64_encoded_dependencies>"
}
```

**Expected response:**

```json
{
  "signature": "<base64_encoded_signature>"
}
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Signature successfully generated. |
| 400 | Invalid Base64 content. |
| 401 | Missing or invalid authentication token. |
| 422 | Request validation error. |

## 8. Certificate Management

### 8.1. Retrieve the Public Signing Key

**Method:** `GET`

**Route:** `/.well-known/public-key`

**Authentication:** Not required.

**Purpose:**

Exposes the public key used by the application to verify certificate signatures.

The endpoint returns:
- The key identifier (`kid`).
- The signing algorithm (`alg`).
- The public key in PEM format (`public_key`).

**Request body:**

None.

**Expected response:**

```json
{
  "kid": "<key_identifier>",
  "alg": "Ed25519",
  "public_key": "<public_key_in_PEM_format>"
}
```

**Possible errors:**

No explicit HTTP errors are raised by this controller. Server-side configuration or key-loading failures may still result in a server error.

### 8.2. Verify a Certificate

**Method:** `POST`

**Route:** `/certificate/verify`

**Authentication:** Not required.

**Purpose:**

Verifies the digital signature of a certificate using the application's public signing key.

The endpoint receives a `SignedCertificateModel`, corresponding to the signed certificate content (for example, the content encoded in a QR code).

**Request body:**

`SignedCertificateModel`.

The exact JSON structure is defined in `schema/certificate_model.py`.

**Expected response:**

If the signature is valid:

```json
{
  "valid": true,
  "payload": {
    "example": "certificate_payload"
  }
}
```

If the signature is invalid or the key is unknown:

```json
{
  "valid": false,
  "reason": "Invalid signature or unknown key."
}
```

**Possible errors:**

| HTTP status | Description |
|---|---|
| 200 | Verification completed. The response indicates whether the signature is valid. |
| 422 | Request validation error. |

## 9. Notes and Implementation Details

- Protected endpoints require a valid access token.
- Project and audit resources are checked against the authenticated user's ownership.
- HMAC signatures and file contents are transmitted using Base64 encoding.
- Regenerating a project's HMAC key invalidates the previous key.
- Certificate signatures use the Ed25519 algorithm.
- The public signing key is exposed through `/.well-known/public-key`.
- Certificate verification is available without user authentication.

For exact request and response schemas, refer to the corresponding files in the `schema/` directory.

# 🏛️ Architecture

The backend follows a **Layered Architecture (N-Tier)** to ensure separation of concerns and maintainability.

| Layer | Directory | Responsibility |
|---|---|---|
| Business Objects | `business_object/` | Represents domain entities |
| Controllers | `controller/` | Handles HTTP requests and routing via FastAPI |
| Services | `service/` | Contains the core business logic |
| DAO | `dao/` | Manages database interactions |
| API_OSV | `api_osv/` | Handles external OSV API interactions |
| API_DEPS_DEV | `api_deps_dev/` | Handles external Deps.dev API interactions |
| Schemas | `schema/` | Defines request and response contracts using Pydantic |

## Architecture diagrams

Add updated sequence diagrams here to illustrate the main application workflows.

Recommended diagrams:
- Project import and authentication.
- User creation and authentication.
- Project audit and analysis.
- Database interactions.

*Note: Sequence diagrams must reflect the current implementation.*

---

# ⚙️ Development Toolkit

## Debugging & Logs

The application uses a structured logging system.

Logs are written to `backend/logs/` and follow the configuration defined in `logging_config.yml`.

A custom `@log` decorator is available to automatically log method inputs and outputs.

## Unit Tests

Run unit tests:

```bash
uv run --project backend pytest -v
```

## Test Coverage

Generate test coverage:

```bash
uv run --project backend coverage run -m pytest backend
uv run --project backend coverage report -m
uv run --project backend coverage html
```

Open the generated HTML report to inspect coverage.

## Ruff

Format the code:

```bash
uv run --project backend ruff format backend/
```

Check and automatically fix linting issues:

```bash
uv run --project backend ruff check --fix backend/
```

## Pylint

Run static analysis:

```bash
uv run --project backend --extra dev pylint --output-format=colorized --disable=C0114,C0411,C0415,W0718 $(git ls-files 'backend/**/*.py') --fail-under=7.5
```

---

# 📁 Configuration Files

The backend contains several configuration files:

| File | Description |
|---|---|
| `logging_config.yml` | Structured logging configuration |
| `pyproject.toml` | Project metadata and dependency definitions |
| `uv.lock` | Lockfile ensuring reproducible environments |
| `__init__.py` | Marks directories as Python packages |
