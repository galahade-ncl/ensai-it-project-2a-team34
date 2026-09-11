
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
        +id_user: int
        +username: string
        +password: string
        +email: string
    }

    class Project {
        +id_project: int
        +name_project: string
        +user: User
        +codefile: CodeFile
        +dependencyfile: DependencyFile
        +HMACkey: hmac.HMAC
    }

    class File {
        +id_file: int
        +date: datetime
        +path: str
    }

    class CodeFile {
        +id_file: int
        +date: datetime
        +path: str
        +tree: ast.Module
    }

    class DependencyFile {
        +id_file: int
        +date: datetime
        +path: str
        +dependencylist: list[str]
    }


    class Audit {
        +id_audit: int
        +id_project: int
        +date: datetime
        +vulnerabilities: list[Vulnerability]
        +licenses: list[License]
        +anti_patterns: list[AntiPattern]
        +complexity: float
        +energy_consumption_kwh: float
        +carbon_emission_gco2e: float
        +sbom: SBOM
        +quality_gate: QualityGate
    }

    class Vulnerability {
        +id_vulnerability: int
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
    User "1" ..> "0..*" Project : owns
    Project "1" ..> "0..*" Audit : owns

    Project ..> DependencyFile : uses
    Project ..> CodeFile : uses
    DependencyFile ..> File : uses
    CodeFile ..> File : uses

    Audit ..> Vulnerability : uses
    Audit ..> Licence : uses
    Audit ..> AntiPattern : uses
    Audit ..> QualityGate : uses


```
