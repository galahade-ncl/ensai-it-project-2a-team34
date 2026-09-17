
# Diagramme de séquence : Demander un audit


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



