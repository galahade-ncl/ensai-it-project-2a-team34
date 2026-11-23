
# Diagramme physique des données

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    %% Business objects
    class User {
        id_user INT PK
        username VARCHAR50
        password VARCHAR100
        email VARCHAR100
        access_token VARCHAR255
    }

    class Project {
        id_project INT PK
        name_project VARCHAR100
        #id_user INT FK
        secretHMACkey VARCHAR100
    }

    class Audit {
        id_audit INT PK
        #id_project INT FK
        date DATE
        complexity FLOAT
        energy_comsumption FLOAT
        carbon_emission_gco2e FLOAT
        type_qualitygate VARCHAR
        status_qualitygate VARCHAR
        certificate_pdf BYTEA,
        certificate_signed JSONB,
        certificate_id TEXT UNIQUE,
        sbom_content BYTEA,
    }

    %% Relationships
    User "1" -- "0..*" Project : owns
    Project "1" -- "0..*" Audit : owns

```
