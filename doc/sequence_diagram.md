
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

    rect rgb(254, 239, 226)
        Note over Utilisateur,BDD: Créer un user

        Utilisateur->>API: Dépose les informations de l'utilisateur<br/>(username, password, email)
        API->>DAO: Vérifier si le nom existe
        DAO->>BDD: Recherche un utilisateut par le username
        BDD-->>DAO: Résultat de la recherche

        alt Nom déjà utilisé
            DAO-->>API: Nom existant
            API-->>Utilisateur: Erreur : Nom déjà utilisé
        else Nom disponible
            DAO-->>API: Nom disponible
            API->>API: Hashe le mot de passe
            API->>DAO: Crée l'utilisateur
            DAO->>BDD: Enregistre les informations de l'utilisateur
            BDD-->DAO: Utilisateur enregistré
            DAO-->>API: Utilisateur créé
            API-->>Utilisateur: Confirmation de la création du compte
        end
    end

    rect rgb(225, 245, 230)
        Note over Utilisateur,BDD: Importer un projet

        Utilisateur->>API: Dépose un projet
        API->>API: Génère la clé secrète HMAC du projet

        API->>DAO: Crée le projet
        DAO->>BDD: Enregistre le projet et sa clé
        BDD-->>DAO: Projet enregistré
        DAO-->>API: Projet créé
        API-->>Utilisateur: Confirmation de l'importation du projet + <br/>donne la clé secrète HMAC

    end

    rect rgb(225, 255, 255)
        Note over Utilisateur,BDD: Demander une signature HMAC

        Utilisateur->>API: Envoie le code et le fichier de dépendances <br/>+ clé secrète HMAC
        API-->>API: Génèren la signature HMAC
        API-->>Utilisateur: Renvoie la signature

    end

    rect rgb(225, 245, 255)
        Note over Utilisateur,BDD: Demander un audit

        Utilisateur->>API: Envoie le code et le fichier de dépendances <br/>+ signature HMAC
        API->>DAO: Demande le projet et sa clé secrète
        DAO->>BDD: Demande les informations relatives au projet
        BDD-->>DAO: Renvoie les informations et la clé secrète
        DAO-->>API: Renvoie les informations et la clé secrète
        API-->>API: Vérifie la signature HMAC
        alt Signature incorrecte
            API-->>Utilisateur: Erreur : signature incorrecte
        else Signature correcte
            API->>API: Réalise l'audit
            API->>DAO: Crée l'audit
            DAO->>BDD: Enregistre les résultats de l'audit
            BDD-->DAO: Audit enregistré
            DAO-->>API: Audit créé
            API-->>Utilisateur: Renvoie les résultats de l'audit
        end
    end

````



