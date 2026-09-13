
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
        id_user SERIAL PK
        username VARCHAR50
        password VARCHAR100
        email VARCHAR100
    }

    class Project {
        id_project SERIAL PK
        name_project VARCHAR100
        #id_user SERIAL FK
        HMACkey hmac.HMAC  #A vérifier
    }

    class File {
        id_file SERIAL PK
        name_file VARCHAR100
        #id_project SERIAL FK
        type_file VARCHAR50
        date DATE
    }


    class Audit {
        id_audit SERIAL PK
        #id_project SERIAL FK
        date DATE
        complexity FLOAT
        energy_consumption_kwh FLOAT
        carbon_emission_gco2e FLOAT
        sbom SBOM  #A vérifier

    }

    class DetectV{
        #id_audit SERIAL
        #id_vulnerability SERIAL
    
    }

    class DetectL{
        #id_audit SERIAL
        #id_license SERIAL

    }

    class DetectA{
        #id_audit SERIAL
        #id_antipattern SERIAL

    }

    class DetectQ{
        #id_audit SERIAL
        #id_quality_gate SERIAL

    }

    class Vulnerability {
        id_vulnerability SERIAL PK
        nom_vulnerability VARCHAR100
        osv_id INT
        cve_id INT
        severity VARCHAR50
        package VARCHAR50
        version_package VARCHAR50
    }

    class Licence {
        id_license SERIAL PK
        name_license VARCHAR100
        risk_level VARCHAR50
    }

    class AntiPattern {
        id_antipattern SERIAL PK
        type_antipattern VARCHAR50
        line INT
        description VARCHAR50
    }

    class QualityGate {
        id_quality_gate SERIAL PK
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
