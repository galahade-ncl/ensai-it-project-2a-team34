
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
        password VARCHAR50
        email VARCHAR50
    }

    class Project {
        id_project INT PK
        name_project VARCHAR50
        user USER
        HMACkey hmac.HMAC
    }

    class File {
        id_file INT PK
        name_file VARCHAR50
        #id_project INT FK
        type VARCHAR50
        date DATETIME
    }


    class Audit {
        id_audit INT PK
        #id_project INT FK
        date DATETIME
        +complexity: float
        +energy_consumption_kwh: float
        +carbon_emission_gco2e: float
        +sbom: SBOM

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
        nom_vulnerability VARCHAR50
        +osv_id: int
        +cve_id: int
        +severity: str
        +package: str
        +version_package: str
    }

    class Licence {
        +id_license: int
        +name: str
        +risk_level: str
    }

    class AntiPattern {
        +id_antipattern: int
        +type: str
        +line: int
        +description: str
    }

    class QualityGate {
        +id_quality_gate: int
        +max_vulnerabilities: int
        +max_carbon_emission: float
        +status: string
    }



    %% Relationships
    User "1" -- "0..*" Project : owns
    Project "1" -- "0..*" Audit : owns

    Project "1" --> "2" File : uses

    Audit -- DetectV
    DetectV -- Vulnerability

    Audit -- DetectL
    DetectL -- Licence

    Audit -- DetectA
    DetectA -- AntiPattern

    Audit -- DetectQ
    DetectQ -- QualityGate


```
