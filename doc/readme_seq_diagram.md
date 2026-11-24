
# Diagramme de séquence


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

