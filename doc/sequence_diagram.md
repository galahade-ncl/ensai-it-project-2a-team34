
# Diagramme de séquence : Demander un audit


````mermaid
sequenceDiagram
    actor Utilisateur
    participant API
    participant DAO
    participant BDD@{ "type" : "database" }
    Utilisateur-->>API: Demande un audit sur un projet
    API-->>DAO: Demande les fichiers du projet
    DAO-->>BDD: Demande les informations relatives au projet
    DAO-->>API: Envoie les informations liées au projet à auditer
    API-->>Utilisateur: Donne les résultats de l'audit
````

# Diagramme de séquence : Importer un projet

````mermaid
sequenceDiagram
    actor Utilisateur
    participant API
    participant DAO
    participant BDD@{ "type" : "database" }
    Utilisateur-->>API: Dépose un projet
    API-->>DAO: Relaie les informations relatives au projet
    DAO-->>BDD: Enregistre les informations
````

