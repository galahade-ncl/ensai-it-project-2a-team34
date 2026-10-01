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
  "themeCSS": ".cluster:nth-of-type(1) rect {   fill: #b3ccf8 !important; stroke: #3086e8 !important; width: 800px !important; } .cluster:nth-of-type(2) rect { fill: #ccf0ff !important; stroke: #586cff !important; width: 2900px !important; } .cluster:nth-of-type(3) rect { fill: rgb(142, 214, 230) !important; stroke: #63c6c9 !important;} .cluster:nth-of-type(4) rect {   fill: #b2f4fb !important; stroke: #30e8e2 !important; }"}}%%

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
            +get_content(): bool
        }

        class CodeFile {
            +id_file: int
            +date: datetime
            +path: str
            +get_content(): bool
        }

        class DependencyFile {
            +id_file: int
            +date: datetime
            +path: str
            +dependencies: list[Dependency]
            +get_content(): bool
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
            +certificat: Certificate
        }

        namespace VulnerabilityClasses {
            class Dependency {
                +id_dependency: int
                +name: str
                +version: str
            }

            class Vulnerability {
                +id_vulnerability: int
                +osv_id: str
                +cve_id: str | None
            }

            class LowVulnerability {
            }

            class MediumVulnerability {
            }

            class HighVulnerability {
            }

            class CriticalVulnerability {
            }
        }

        class License {
            +id_license: int
            +name: str
            +risk_level: str
        }

        class AntiPattern {
            +id_antipattern: int
            +line: int
            +description: str
        }

        class NestedLoop {
            +depth: int
            }

        class RecursiveCall {
            +function_name: str
        }

        namespace QualityGateClasses{
            class QualityGate {
                + id_quality_gate: int
                + max_vulnerabilities: int
                + max_critical_vulnerabilities: int
                + max_carbon_emission: float
                + max_energy_consumption: float
                + status: string
            }

            class SecurityQualityGate {
                + evaluate(Audit): QualityGate
            }

            class EcoQualityGate {
                + evaluate(Audit): QualityGate
            }

            class GlobalQualityGate {
                + evaluate(Audit): QualityGate
            }
            class QualityGateFactory {
                + get_qualitygate(type: string): QualityGate
            }
        }
        class Certificate {
            +id_certificate: int
            +date: datetime
            +type: string
            +status: string
            +path: string
        }

    }

    %% Relationships
    User "1" ..> "0..*" Project : owns
    Project "1" ..> "0..*" Audit : owns
    DependencyFile ..> Dependency : uses
    Dependency "1" ..> "0..*" Vulnerability : affected by

    Project ..> DependencyFile : uses
    Project ..> CodeFile : uses
    DependencyFile --|> File
    CodeFile --|> File

    Audit ..> Vulnerability : uses
    Audit ..> License : uses
    Audit ..> AntiPattern : uses
    Audit ..> QualityGate : uses

    Vulnerability <|-- LowVulnerability
    Vulnerability <|-- MediumVulnerability
    Vulnerability <|-- HighVulnerability
    Vulnerability <|-- CriticalVulnerability
    AntiPattern <|-- NestedLoop
    AntiPattern <|-- RecursiveCall

    QualityGate <|-- SecurityQualityGate
    QualityGate <|-- EcoQualityGate
    QualityGate <|-- GlobalQualityGate

    QualityGateFactory ..> QualityGate : uses

    Audit "1" --> "0..*" Certificate : owns

    %% Colors

    style User fill:#E3F0FF,stroke:#4A90E2
    style Project fill:#E3F0FF,stroke:#4A90E2
    style File fill:#E3F0FF,stroke:#4A90E2
    style CodeFile fill:#E3F0FF,stroke:#4A90E2
    style DependencyFile fill:#E3F0FF,stroke:#4A90E2
    style Audit fill:#E3F0FF,stroke:#4A90E2
    style Dependency fill:#E3F0FF,stroke:#4A90E2
    style Vulnerability fill:#E3F0FF,stroke:#4A90E2
    style LowVulnerability fill:#E3F0FF,stroke:#4A90E2
    style MediumVulnerability fill:#E3F0FF,stroke:#4A90E2
    style HighVulnerability fill:#E3F0FF,stroke:#4A90E2
    style CriticalVulnerability fill:#E3F0FF,stroke:#4A90E2
    style License fill:#E3F0FF,stroke:#4A90E2
    style AntiPattern fill:#E3F0FF,stroke:#4A90E2
    style NestedLoop fill:#E3F0FF,stroke:#4A90E2
    style RecursiveCall fill:#E3F0FF,stroke:#4A90E2
    style SBOM fill:#E3F0FF,stroke:#4A90E2
    style QualityGate fill:#E3F0FF,stroke:#4A90E2
    style EcoQualityGate fill:#E3F0FF,stroke:#4A90E2
    style SecurityQualityGate fill:#E3F0FF,stroke:#4A90E2
    style GlobalQualityGate fill:#E3F0FF,stroke:#4A90E2
    style QualityGateFactory fill:#E3F0FF,stroke:#4A90E2
    style Certificate fill:#E3F0FF,stroke:#4A90E2
```
