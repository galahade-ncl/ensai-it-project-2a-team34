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
  "themeCSS": ".cluster:nth-of-type(1) rect {   fill: #b3ccf8 !important; stroke: #3086e8 !important; width: 1200px !important; } .cluster:nth-of-type(2) rect { fill: #ccf0ff !important; stroke: #586cff !important; width: 2900px !important; } .cluster:nth-of-type(3) rect { fill: rgb(241, 254, 245) !important; stroke: #217a34 !important;} .cluster:nth-of-type(4) rect { fill: rgba(179, 255, 188, 0.8) !important; stroke: #3ea053 !important;} .cluster:nth-of-type(5) rect {   fill: #b2f4fb !important; stroke: #30e8e2 !important; } .cluster:nth-of-type(6) rect {   fill: rgb(142, 214, 230) !important; stroke: #63c6c9 !important; }"}}%%

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
            +secretHMACkey: bytes
        }

        class File {
            +get_duty(): str
        }

        class CodeFile {
            +name: str
            +content: bytes
            +type_file: str
            +date: datetime
            +get_duty(self): str
        }

        class DependencyFile {
            +name: str
            +content: bytes
            +type_file: str
            +date: datetime[Dependency]
            +get_duty(self): str
        }
        class SbomFile {
            +name: str
            +content: bytes
            +type_file: str
            +date: datetime[Dependency]
            +get_duty(self): str
            }
    }

    namespace AuditClasses {
        class Audit {
            +id_audit: int
            +id_project: int
            +date: datetime
            +vulnerabilities: list[Vulnerability]
            +licenses: list[Licence]
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
                +package: str
                +version_package: str
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

        class Licence {
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
                + evaluate(audit: Audit): bool
                + get_type(self) -> str

            }

            class SecurityQualityGate {
                + max_vulnerabilities: int
                + max_critical_vulnerabilities: int
                + status: string
                + evaluate(audit: Audit): bool
                + get_type(self) -> str
            }

            class EcoQualityGate {
                + max_carbon_emission: float
                + max_energy_consumption: float
                + status: string
                + evaluate(audit: Audit): bool
                + get_type(self) -> str
            }

            class GlobalQualityGate {
                + max_vulnerabilities: int
                + max_critical_vulnerabilities: int
                + max_carbon_emission: float
                + max_energy_consumption: float
                + status: string
                + evaluate(audit: Audit): bool
                + get_type(self) -> str
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
        +upload(project_name: str, user: User): Project | None
        +find_by_id(id_project: int): Project | None
        +list_all_project(id_user: int): list[Project]
        +update(project: Project): Project | None
        +delete(project: Project): bool
        +verify_signature(project: Project, code: bytes, dependency: bytes, signature: bytes): bool
    }

    namespace FileServices {
        class FileService {
            +get_content(file: File): bool
            +get_filename(self, dependencyfile: DependencyFile) -> str
            +parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]
            +parse_ast(self, codefile: CodeFile) -> ast.Module
        }
        class JavaService {
            +parse_ast(self, content: bytes) -> ast.Module
            }
        class JsService {
            +parse_ast(self, content: bytes) -> ast.Module
            }
        class JsonService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
        class PyService {
            +parse_ast(self, content: bytes) -> ast.Module
            }
        class TomlService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
        class TxtService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
        class XmlService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
    }

    class AuditService {
        +create(int, int, datetime, list[Vulnerability], licenses: list[Licence], list[AntiPattern],float, sbom, float, float, QualityGate, list[Certificate]): Audit
        +list_all_audit(id_audit: int) : list[Audit]
        +find_by_id(id_audit: int): Audit
        +run_audit(project: Project): Audit
    }

    class SecurityService {
        +detect_ecosystem(dependencyfile: DependencyFile) -> str
        +find_vulnerabilities(list[Dependency]): list[Vulnerability]
        +find_licenses(dependencyfile: DependencyFile): list[Licence]
    }

    class EcoService {
        +detect_antipatterns(ast.Module): list[AntiPattern]
        +estimate_complexity(ast.Module): float
        +calculate_energy(ast.Module): float
        +calculate_carbon(ast.Module): float
    }

    class SbomService {
        +generate(project: Project): SBOM
    }

    class QualityGateService {
        +evaluate(audit: Audit): bool
    }

    class CertificateService {
        +generate_certificate(audit: Audit): Certificate
        }

    class VulnerabilityService {
        +get_critical_vulnerability_count(audit: Audit): int
        }

    %% API Externes
    namespace ExternalAPI {
        class API_OSV {
            +find_vulnerabilities(Dependency): list[Vulnerability]
            +_get_severity(osv_vuln: dict) -> str | None
            +_to_vulnerability(osv_vuln: dict, dependency: Dependency, severity: str) -> Vulnerability
        }
        class API_DEPSDEV{
            +clean_version(version: str | None) -> str | None
            +find_licences(dependency: Dependency, ecosystem: str) -> list[str]
            +_default_version(base: str) -> str | None
            +_to_licence(licence_name: str) -> Licence
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
    SbomFile --|> File

    Audit ..> Vulnerability : uses
    Audit ..> Licence : uses
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

    FileService ..> File : uses
    FileService ..> JavaService : uses
    FileService ..> JsService : uses
    FileService ..> JsonService : uses
    FileService ..> PyService : uses
    FileService ..> TomlService : uses
    FileService ..> TxtService : uses
    FileService ..> XmlService : uses


    SecurityService ..> API_OSV : uses
    API_OSV ..> Dependency : analyse
    API_OSV ..> Vulnerability : return

    SecurityService ..> API_DEPSDEV : uses
    API_DEPSDEV ..> Dependency : analyse
    API_DEPSDEV ..> Licence : return

    UserService ..> UserDAO : calls
    UserService ..> User : uses
    UserService ..> Project : uses
    UserDAO ..> User : uses
    API ..> UserService : calls
    ProjectService ..> Project : uses
    ProjectService ..> ProjectDAO : calls
    ProjectService ..> FileService : uses
    ProjectService ..> File : uses
    ProjectService ..> User : uses
    ProjectService ..> UserDAO : calls
    ProjectService ..> Audit : uses
    ProjectService ..> AuditDAO : calls
    ProjectDAO ..> Project : uses
    API ..> ProjectService : calls
    AuditService ..> Audit : uses
    AuditService ..> AuditDAO : calls
    AuditService ..> File : uses
    AuditDAO ..> Audit : uses
    AuditDAO ..> VulnerabilityService : calls
    VulnerabilityService ..> Vulnerability : uses
    API ..> AuditService : calls

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SbomService : uses
    AuditService ..> CertificateService : uses

    QualityGateService ..> QualityGateFactory : uses
    QualityGateService ..> QualityGate : uses
    QualityGateService ..> Audit : analyzes
    CertificateService ..> Certificate : uses
    SbomService ..> Project : uses
    SbomService ..> SbomFile : create
    SecurityService ..> Dependency : uses
    SecurityService ..> Vulnerability : uses
    SecurityService ..> Licence : uses
    SecurityService ..> DependencyFile : uses
    EcoService ..> AntiPattern : uses
    EcoService ..> CodeFile : uses

    %% Colors

    style User fill:#E3F0FF,stroke:#4A90E2
    style Project fill:#E3F0FF,stroke:#4A90E2
    style File fill:#E3F0FF,stroke:#4A90E2
    style CodeFile fill:#E3F0FF,stroke:#4A90E2
    style DependencyFile fill:#E3F0FF,stroke:#4A90E2
    style SbomFile fill:#E3F0FF,stroke:#4A90E2
    style Audit fill:#E3F0FF,stroke:#4A90E2
    style Dependency fill:#E3F0FF,stroke:#4A90E2
    style Vulnerability fill:#E3F0FF,stroke:#4A90E2
    style LowVulnerability fill:#E3F0FF,stroke:#4A90E2
    style MediumVulnerability fill:#E3F0FF,stroke:#4A90E2
    style HighVulnerability fill:#E3F0FF,stroke:#4A90E2
    style CriticalVulnerability fill:#E3F0FF,stroke:#4A90E2
    style Licence fill:#E3F0FF,stroke:#4A90E2
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
    style API_OSV fill:#E3F0FF,stroke:#4A90E2


    style UserDAO fill:#FFF3E0,stroke:#FB8C00
    style ProjectDAO fill:#FFF3E0,stroke:#FB8C00
    style AuditDAO fill:#FFF3E0,stroke:#FB8C00


    style UserService fill:#E8F5E9,stroke:#43A047
    style ProjectService fill:#E8F5E9,stroke:#43A047

    style FileService fill:#E8F5E9,stroke:#43A047
    style JavaService fill:#E8F5E9,stroke:#43A047
    style JsService fill:#E8F5E9,stroke:#43A047
    style JsonService fill:#E8F5E9,stroke:#43A047
    style PyService fill:#E8F5E9,stroke:#43A047
    style TomlService fill:#E8F5E9,stroke:#43A047
    style TxtService fill:#E8F5E9,stroke:#43A047
    style XmlService fill:#E8F5E9,stroke:#43A047

    style AuditService fill:#E8F5E9,stroke:#43A047
    style SecurityService fill:#E8F5E9,stroke:#43A047
    style EcoService fill:#E8F5E9,stroke:#43A047
    style SbomService fill:#E8F5E9,stroke:#43A047
    style QualityGateService fill:#E8F5E9,stroke:#43A047
    style VulnerabilityService fill:#E8F5E9,stroke:#43A047
    style CertificateService fill:#E8F5E9,stroke:#43A047
    style API_OSV fill:#E8F5E9,stroke:#43A047
    style API_DEPSDEV fill:#E8F5E9,stroke:#43A047

    style API fill:#F3E5F5,stroke:#8E44AD,color:#000
```
