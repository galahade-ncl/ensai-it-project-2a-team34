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
  "themeCSS": ".cluster:nth-of-type(1) rect {   fill: #b3ccf8 !important; stroke: #3086e8 !important; width: 800px !important; } .cluster:nth-of-type(2) rect { fill: #ccf0ff !important; stroke: #586cff !important; width: 2900px !important; } .cluster:nth-of-type(3) rect { fill: rgb(241, 254, 245) !important; stroke: #3ea053 !important;} .cluster:nth-of-type(4) rect { fill: rgb(142, 214, 230) !important; stroke: #63c6c9 !important;} .cluster:nth-of-type(5) rect {   fill: #b2f4fb !important; stroke: #30e8e2 !important; }"}}%%

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
            +codefile: CodeFile | None
            +dependencyfile: DependencyFile | None
            +HMACkey: hmac.HMAC
        }

        class File {
            +get_content(): bool
            +get_type(): str
        }

        class CodeFile {
            +id_file: int
            +date: datetime
            +path: str
            +get_content(): bool
            +get_type(): str
        }

        class DependencyFile {
            +id_file: int
            +date: datetime
            +path: str
            +dependencies: list[Dependency]
            +get_content(): bool
            +get_type(): str
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
                + evaluate(Audit): bool

            }

            class SecurityQualityGate {
                + id_quality_gate: int
                + max_vulnerabilities: int
                + max_critical_vulnerabilities: int
                + status: string
                + evaluate(Audit): bool
            }

            class EcoQualityGate {
                + id_quality_gate: int
                + max_carbon_emission: float
                + max_energy_consumption: float
                + status: string
                + evaluate(Audit): bool
            }

            class GlobalQualityGate {
                + id_quality_gate: int
                + max_vulnerabilities: int
                + max_critical_vulnerabilities: int
                + max_carbon_emission: float
                + max_energy_consumption: float
                + status: string
                + evaluate(Audit): bool
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


    %% Data Access Objects
    class UserDAO {
        +create(User): bool
        +find_by_id(int): User
        +update(User): User
        +delete(User): bool
        +login(str,str): User
    }

    class ProjectDAO {
        +upload(Project): bool
        +find_by_id(int): Project
        +list_all_project(int): list[Project]
        +update(Project): Project
        +delete(Project): bool
    }

    class FileDAO {
        +create(File): bool
        +find_by_id(int): File
        +find_all_by_project(int): list[File]
        +update(File): File
        +delete(File): bool
    }
    class AuditDAO {
        +create(Audit): bool
        +find_by_id(int): Audit
        +find_all(int): list[Audit]
    }

    %% Service layer
    class UserService {
        +create(str,str,str): User
        +find_by_id(int): User
        +update(User): User
        +delete(User): bool
        +login(str,str): User
        +username_already_used(str): bool
    }

    class ProjectService {
        +upload(int, str, User, Optional : CodeFile, Optional : DependencyFile): Project, hmac.HMAC
        +upload_dependency_file(int, datetime, str, int): DependencyFile
        +upload_code_file(int, datetime, str, int): CodeFile
        +find_by_id(int): Project
        +list_all_project(int): list[Project]
        +update(Project): Project
        +delete(Project): bool
        +generate_HMAC_key(): hmac.HMAC
        +verify_signature(Project, bytes): bool
    }

    class FileService {
        +create_file(int, datetime, str, int): File
        +find_by_id(int): File
        +find_all_by_project(int): list[File]
        +find_user(int): User
        +find_project(int): Project
        +update(File): File
        +delete(File): bool
        +get_content(): bool
    }

    class AuditService {
        +create(int, int, datetime, list[Vulnerability], list[License], list[AntiPattern], float, float, float, QualityGate, list[Certificate]): Audit
        +list_all_audit(int) : list[Audit]
        +find_by_id(int): Audit
        +run_audit(Project): Audit
    }

    class SecurityService {
        +parse_dependencies(DependencyFile): list[Dependency]
        +find_vulnerabilities(list[Dependency]): list[Vulnerability]
        +find_licenses(DependencyFile): list[License]
    }

    class EcoService {
        +parse_ast(CodeFile): ast.Module
        +detect_antipatterns(ast.Module): list[AntiPattern]
        +estimate_complexity(ast.Module): float
        +calculate_energy(): float
        +calculate_carbon(): float
    }

    class SBOMService {
        +generate(Project): SBOM
    }

    class QualityGateService {
        +evaluate(Audit): bool
        +generate_certificate(Audit): Certificate
    }

    %% API Externe
    namespace ExternalAPI {
        class OSVClient {
            +find_vulnerabilities(Dependency): list[Vulnerability]
        }
    }

    %% API
    class API {
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
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

    SecurityService ..> OSVClient : uses
    OSVClient ..> Dependency : analyze
    OSVClient ..> Vulnerability : return

    QualityGateFactory ..> QualityGate : uses

    Audit "1" --> "0..*" Certificate : owns

    UserService ..> UserDAO : calls
    UserService ..> User : uses
    UserService ..> FileDAO : calls
    UserService ..> Project : uses
    UserDAO ..> User : uses
    API ..> UserService : calls
    FileService ..> File : uses
    FileService ..> FileDAO : calls
    ProjectService ..> Project : uses
    ProjectService ..> ProjectDAO : calls
    ProjectService ..> FileService : uses
    ProjectService ..> FileDAO : calls
    ProjectService ..> File : uses
    ProjectService ..> User : uses
    ProjectService ..> UserDAO : calls
    ProjectService ..> Audit : uses
    ProjectService ..> AuditDAO : calls
    ProjectDAO ..> Project : uses
    FileDAO ..> File : uses
    API ..> ProjectService : calls
    AuditService ..> Audit : uses
    AuditService ..> AuditDAO : calls
    AuditService ..> File : uses
    AuditService ..> FileDAO : calls
    AuditDAO ..> Audit : uses
    API ..> AuditService : calls

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SBOMService : uses

    QualityGateService ..> QualityGateFactory : uses
    QualityGateService ..> QualityGate : uses
    QualityGateService ..> Audit : analyzes
    QualityGateService ..> Certificate : uses
    SBOMService ..> Project : uses
    SecurityService ..> Dependency : uses
    SecurityService ..> Vulnerability : uses
    SecurityService ..> License : uses
    SecurityService ..> DependencyFile : uses
    EcoService ..> AntiPattern : uses
    EcoService ..> CodeFile : uses

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
    style OSVClient fill:#E3F0FF,stroke:#4A90E2

    style UserDAO fill:#FFF3E0,stroke:#FB8C00
    style FileDAO fill:#FFF3E0,stroke:#FB8C00
    style ProjectDAO fill:#FFF3E0,stroke:#FB8C00
    style AuditDAO fill:#FFF3E0,stroke:#FB8C00

    style UserService fill:#E8F5E9,stroke:#43A047
    style ProjectService fill:#E8F5E9,stroke:#43A047
    style FileService fill:#E8F5E9,stroke:#43A047
    style AuditService fill:#E8F5E9,stroke:#43A047
    style SecurityService fill:#E8F5E9,stroke:#43A047
    style EcoService fill:#E8F5E9,stroke:#43A047
    style SBOMService fill:#E8F5E9,stroke:#43A047
    style QualityGateService fill:#E8F5E9,stroke:#43A047
    style OSVClient fill:#E8F5E9,stroke:#43A047

    style API fill:#F3E5F5,stroke:#8E44AD,color:#000
```
