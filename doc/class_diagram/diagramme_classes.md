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
        +username: str
        +password: str
        +email: str
        +access_token: str
    }

    namespace ProjectClasses {
        class Project {
            +id_project: int
            +name_project: str
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
            +date: datetime
            +get_duty(self): str
        }
        class SbomFile {
            +name: str
            +content: bytes
            +type_file: str
            +date: datetime
            +get_duty(self): str
            }
        class CertificateFile {
            +name: str
            +content: bytes
            +type_file: str
            +qualitygate_type: str
            +date: datetime
            +signed_data: dict | None
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
            +sbom: SbomFile
            +quality_gate: QualityGate
            +certificate: CertificateFile | None
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

            class Severity {
                <<enumeration>>
                LOW
                MEDIUM
                HIGH
                CRITICAL
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

        class AstAnalysis {
            +metrics: dict
            +antipatterns: list[AntiPattern]
            +complexity: float
            +energy_kwh: float
            +carbon_gco2e: float
        }

        class MachineType {
            <<enumeration>>
            REFERENCE
            LAPTOP
            DESKTOP_HIGH_END
            RASPBERRY_PI
            REFERENCE_WORLD_MIX
            +operations_per_second: int
            +cpu_power_w: float
            +carbon_intensity_gco2e_per_kwh: float
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
                + get_qualitygate(type_qualitygate: str, max_vulnerabilities: int, max_critical_vulnerabilities: int, max_carbon_emission: float, max_energy_consumption: float, status: str): QualityGate
            }
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
        +update_secret_key(Project): bool
        +delete(Project): bool
    }

    class AuditDAO {
        +create(Audit): bool
        +find_by_id(int): Audit
        +find_all(): list[Audit]
        +list_all_audit(Project): list[Audit]
        +update(Audit): bool
        +delete(Audit): bool
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
        +find_by_id_and_user(id_project: int, id_user: int): Project | None
        +list_all_project(id_user: int): list[Project]
        +update(project: Project): Project | None
        +delete(project: Project): bool
        +verify_signature(project: Project, signature: bytes): bool
        +regenerate_secret_key(project: Project): str | None
    }

    namespace FileServices {
        class FileService {
            +get_filename(self, dependencyfile: DependencyFile) -> str
            +parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]
        }
        class JsonService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
        class TomlService {
            +parse_dependencies(self, content: bytes) -> list[Dependency]
            }
        class LockService {
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
        +create(int, datetime, list[Vulnerability], list[Licence], list[AntiPattern], float, float, float, SbomFile, QualityGate, CertificateFile | None): Audit
        +find_by_id(id_audit: int): Audit
        +list_all_audit(id_project: int): list[Audit]
        +update(audit: Audit): bool
        +run_audit(project: Project, quality_gate_type: str, machine_type: MachineType): Audit
    }

    class SecurityService {
        +detect_ecosystem(dependencyfile: DependencyFile) -> str
        +find_vulnerabilities(dep_file: DependencyFile): list[Vulnerability]
        +find_licences(dep_file: DependencyFile): list[Licence]
    }

    class EcoService {
        +machine_type: MachineType
        +parse(code_file: CodeFile): ast.Module
        +analyze(code_file: CodeFile, input_size: int): AstAnalysis
        +detect_antipatterns(tree: ast.Module): list[AntiPattern]
        +estimate_complexity(tree: ast.Module): float
        +calculate_energy(metrics: dict, input_size: int): float
        +calculate_carbon(energy_kwh: float): float
    }

    class SbomService {
        +generate(project: Project, vulnerabilities: list[Vulnerability]): SbomFile
        +create_empty_sbom(): SbomFile
    }

    class QualityGateService {
        +create(type_qualitygate: str, max_vulnerabilities: int, max_critical_vulnerabilities: int, max_carbon_emission: float, max_energy_consumption: float, status: str): QualityGate
        +evaluate(qualitygate: QualityGate, audit: Audit)
    }

    class CertificateService {
        +generate_certificate(audit: Audit, project: Project, qualitygate_type: str): CertificateFile
        +sign_certificate(payload: dict): dict
        +verify_certificate(certificate: dict): bool
        }

    class VulnerabilityService {
        +get_critical_vulnerability_count(audit: Audit): int
        }

    %% API Externes
    namespace ExternalAPI {
        class API_OSV {
            +find_vulnerabilities(dependency: Dependency, ecosystem: str): list[Vulnerability]
            +_get_severity(osv_vuln: dict) -> str | None
            +_to_vulnerability(osv_vuln: dict, dependency: Dependency, severity: str) -> Vulnerability
        }
        class API_DEPSDEV{
            +clean_version(version: str | None) -> str | None
            +find_licences(dependency: Dependency, ecosystem: str) -> list[Licence]
            +_default_version(base: str) -> str | None
            +_to_licences(names: list[str]) -> list[Licence]
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
    CertificateFile --|> File

    Audit ..> Vulnerability : uses
    Audit ..> Licence : uses
    Audit ..> AntiPattern : uses
    Audit ..> QualityGate : uses
    Audit ..> SbomFile : uses

    Vulnerability <|-- LowVulnerability
    Vulnerability <|-- MediumVulnerability
    Vulnerability <|-- HighVulnerability
    Vulnerability <|-- CriticalVulnerability
    Severity ..> Vulnerability : gives the class of
    AntiPattern <|-- NestedLoop
    AntiPattern <|-- RecursiveCall

    QualityGate <|-- SecurityQualityGate
    QualityGate <|-- EcoQualityGate
    QualityGate <|-- GlobalQualityGate

    QualityGateFactory ..> QualityGate : creates

    Audit "1" --> "0..1" CertificateFile : owns

    FileService ..> File : uses
    FileService ..> JsonService : uses
    FileService ..> TomlService : uses
    FileService ..> LockService : uses
    FileService ..> TxtService : uses
    FileService ..> XmlService : uses


    SecurityService ..> API_OSV : uses
    API_OSV ..> Dependency : analyse
    API_OSV ..> Vulnerability : return
    API_OSV ..> Severity : uses

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
    AuditDAO ..> QualityGateService : calls
    AuditDAO ..> SbomService : calls
    AuditDAO ..> CertificateFile : uses
    VulnerabilityService ..> Vulnerability : uses
    API ..> AuditService : calls
    API ..> CertificateService : calls
    API ..> MachineType : lists

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SbomService : uses
    AuditService ..> CertificateService : uses
    AuditService ..> MachineType : uses

    QualityGateService ..> QualityGateFactory : uses
    QualityGateService ..> QualityGate : uses
    QualityGateService ..> Audit : analyzes
    CertificateService ..> CertificateFile : creates
    CertificateService ..> Audit : uses
    CertificateService ..> Project : uses
    SbomService ..> Project : uses
    SbomService ..> SbomFile : create
    SbomService ..> FileService : uses
    SbomService ..> Vulnerability : uses
    SecurityService ..> Dependency : uses
    SecurityService ..> Vulnerability : uses
    SecurityService ..> Licence : uses
    SecurityService ..> DependencyFile : uses
    SecurityService ..> FileService : uses
    EcoService ..> AntiPattern : uses
    EcoService ..> CodeFile : uses
    EcoService ..> MachineType : uses
    EcoService ..> AstAnalysis : returns

    %% Colors

    style User fill:#E3F0FF,stroke:#4A90E2
    style Project fill:#E3F0FF,stroke:#4A90E2
    style File fill:#E3F0FF,stroke:#4A90E2
    style CodeFile fill:#E3F0FF,stroke:#4A90E2
    style DependencyFile fill:#E3F0FF,stroke:#4A90E2
    style SbomFile fill:#E3F0FF,stroke:#4A90E2
    style CertificateFile fill:#E3F0FF,stroke:#4A90E2
    style Audit fill:#E3F0FF,stroke:#4A90E2
    style Dependency fill:#E3F0FF,stroke:#4A90E2
    style Vulnerability fill:#E3F0FF,stroke:#4A90E2
    style LowVulnerability fill:#E3F0FF,stroke:#4A90E2
    style MediumVulnerability fill:#E3F0FF,stroke:#4A90E2
    style HighVulnerability fill:#E3F0FF,stroke:#4A90E2
    style CriticalVulnerability fill:#E3F0FF,stroke:#4A90E2
    style Severity fill:#E3F0FF,stroke:#4A90E2
    style Licence fill:#E3F0FF,stroke:#4A90E2
    style AntiPattern fill:#E3F0FF,stroke:#4A90E2
    style NestedLoop fill:#E3F0FF,stroke:#4A90E2
    style RecursiveCall fill:#E3F0FF,stroke:#4A90E2
    style AstAnalysis fill:#E3F0FF,stroke:#4A90E2
    style MachineType fill:#E3F0FF,stroke:#4A90E2
    style QualityGate fill:#E3F0FF,stroke:#4A90E2
    style EcoQualityGate fill:#E3F0FF,stroke:#4A90E2
    style SecurityQualityGate fill:#E3F0FF,stroke:#4A90E2
    style GlobalQualityGate fill:#E3F0FF,stroke:#4A90E2
    style QualityGateFactory fill:#E3F0FF,stroke:#4A90E2


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
    style LockService fill:#E8F5E9,stroke:#43A047
    style TxtService fill:#E8F5E9,stroke:#43A047
    style XmlService fill:#E8F5E9,stroke:#43A047

    style AuditService fill:#E8F5E9,stroke:#43A047
    style SecurityService fill:#E8F5E9,stroke:#43A047
    style EcoService fill:#E8F5E9,stroke:#43A047
    style SbomService fill:#E8F5E9,stroke:#43A047
    style QualityGateService fill:#E8F5E9,stroke:#43A047
    style VulnerabilityService fill:#E8F5E9,stroke:#43A047
    style CertificateService fill:#E8F5E9,stroke:#43A047
    style Security fill:#E8F5E9,stroke:#43A047
    style API_OSV fill:#E8F5E9,stroke:#43A047
    style API_DEPSDEV fill:#E8F5E9,stroke:#43A047

    style API fill:#F3E5F5,stroke:#8E44AD,color:#000
```
