# Diagramme de classes des objets métiers

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

%%{init: {
  "theme": "base",
  "flowchart": {
    "htmlLabels": true,
    "curve": "basis"},
  "themeCSS": ".cluster:nth-of-type(1) rect {   fill: #b3ccf8 !important; stroke: #3086e8 !important; width: 700px !important; } .cluster:nth-of-type(2) rect { fill: #ccf0ff !important; stroke: #586cff !important; width: 1100px !important; } .cluster:nth-of-type(3) rect { fill: #e1baf1 !important; stroke: #8E44AD !important;}"}}%%

classDiagram
    %% Business objects
    class User {
        +id_user: int
        +username: string
        +password: string
        +email: string
    }

    namespace ProjectClasses {
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
            +submit(): bool
        }

        class CodeFile {
            +id_file: int
            +date: datetime
            +path: str
            +tree: ast.Module
            +submit(): bool
        }

        class DependencyFile {
            +id_file: int
            +date: datetime
            +path: str
            +dependencylist: list[str]
            +submit(): bool
        }
    }

    namespace AuditClasses {
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
            +osv_id: str
            +cve_id: str | None
            +severity: str
            +package: str
            +version_package: str
        }

        class License {
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
            +max_critical_vulnerabilities: int
            +max_carbon_emission: float
            +status: string
        }
    }

    %% Relationships
    User "1" ..> "0..*" Project : owns
    Project "1" ..> "0..*" Audit : owns

    Project ..> DependencyFile : uses
    Project ..> CodeFile : uses
    DependencyFile ..> File : uses
    CodeFile ..> File : uses

    Audit ..> Vulnerability : uses
    Audit ..> License : uses
    Audit ..> AntiPattern : uses
    Audit ..> QualityGate : uses

    %% Colors

    style User fill:#E3F0FF,stroke:#4A90E2
    style Project fill:#E3F0FF,stroke:#4A90E2
    style File fill:#E3F0FF,stroke:#4A90E2
    style CodeFile fill:#E3F0FF,stroke:#4A90E2
    style DependencyFile fill:#E3F0FF,stroke:#4A90E2
    style Audit fill:#E3F0FF,stroke:#4A90E2
    style Vulnerability fill:#E3F0FF,stroke:#4A90E2
    style License fill:#E3F0FF,stroke:#4A90E2
    style AntiPattern fill:#E3F0FF,stroke:#4A90E2
    style SBOM fill:#E3F0FF,stroke:#4A90E2
    style QualityGate fill:#E3F0FF,stroke:#4A90E2
```
