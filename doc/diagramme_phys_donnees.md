
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
    }

    class Project {
        id_project INT PK
        name_project VARCHAR100
        #id_user INT FK
        HMACkey hmac.HMAC  #A vérifier
    }

    class File {
        id_file INT PK
        name_file VARCHAR100
        #id_project INT FK
        type_file VARCHAR50
        date DATE
    }


    class Audit {
        id_audit INT PK
        #id_project INT FK
        date DATE
        complexity FLOAT
        energy_consumption_kwh FLOAT
        carbon_emission_gco2e FLOAT
        sbom SBOM  #A vérifier

    }

    class DetectV{
        #id_audit INT
        #id_vulnerability INT
    
    }

    class DetectL{
        #id_audit INT
        #id_license INT

    }

    class DetectA{
        #id_audit INT
        #id_antipattern INT

    }

    class DetectQ{
        #id_audit INT
        #id_quality_gate INT

    }

    class Vulnerability {
        id_vulnerability INT PK
        nom_vulnerability VARCHAR100
        osv_id INT
        cve_id INT
        severity VARCHAR50
        package VARCHAR50
        version_package VARCHAR50
    }

    class Licence {
        id_license INT PK
        name_license VARCHAR100
        risk_level VARCHAR50
    }

    class AntiPattern {
        id_antipattern INT PK
        type_antipattern VARCHAR50
        line INT
        description VARCHAR50
    }

    class QualityGate {
        id_quality_gate INT PK
        max_vulnerabilities INT
        max_carbon_emission FLOAT
        status VARCHAR50
    }



    %% Relationships
    User "1" -- "0..*" Project : owns
    Project "1" -- "0..*" Audit : owns

    Project "1" --> "2" File : uses

    Audit "1" -- "0..*" DetectV
    Vulnerability "1" -- "0..*" DetectV

    Audit "1" -- "0..*" DetectL
    Licence "1" -- "0..*" DetectL

    Audit "1" -- "0..*" DetectA
    AntiPattern "1" -- "0..*" DetectA

    Audit "1" -- "0..*" DetectQ
    QualityGate "1" -- "0..*" DetectQ


```
