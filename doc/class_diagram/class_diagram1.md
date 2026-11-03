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
  "themeCSS": " .cluster:nth-of-type(1) rect { fill: rgb(241, 254, 245) !important; stroke: #3ea053 !important;} .cluster:nth-of-type(2) rect { fill: rgba(179, 255, 188, 0.8) !important; stroke: #3ea053 !important;} "}}%%

classDiagram

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
    FileService ..> JavaService : uses
    FileService ..> JsService : uses
    FileService ..> JsonService : uses
    FileService ..> PyService : uses
    FileService ..> TomlService : uses
    FileService ..> TxtService : uses
    FileService ..> XmlService : uses


    SecurityService ..> API_OSV : uses

    SecurityService ..> API_DEPSDEV : uses

    UserService ..> UserDAO : calls
    API ..> UserService : calls
    ProjectService ..> ProjectDAO : calls
    ProjectService ..> FileService : uses
    ProjectService ..> UserDAO : calls
    ProjectService ..> AuditDAO : calls
    API ..> ProjectService : calls
    AuditService ..> AuditDAO : calls
    AuditDAO ..> VulnerabilityService : calls
    API ..> AuditService : calls

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SbomService : uses
    AuditService ..> CertificateService : uses

    %% Colors

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
