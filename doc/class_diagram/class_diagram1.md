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
  "themeCSS": " .cluster:nth-of-type(1) rect { fill: rgb(241, 254, 245) !important; stroke: #3ea053 !important;} "}}%%

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

    class FileDAO {
        +create(File): bool
        +find_by_id(int): File
        +find_all(): list[File]
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
        +upload(int, string, User, CodeFile, DependencyFile, hmac.HMAC): Project
        +upload_dependency_file(int, datetime, str, list[str]): DependencyFile
        +upload_code_file(int, datetime, str, ast.Module): CodeFile
        +find_by_id(int): Project
        +list_all_project(int): list[Project]
        +update(Project): Project
        +delete(Project): bool
        +generate_HMAC_key(): bytes
        +verify_signature(Project, bytes): bool
    }

    class FileService {
        +create_file(int, datetime, str): File
        +find_by_id(int): File
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

    SecurityService ..> OSVClient : uses

    UserService ..> UserDAO : calls
    UserService ..> FileDAO : calls
    API ..> UserService : calls
    FileService ..> FileDAO : calls
    ProjectService ..> ProjectDAO : calls
    ProjectService ..> FileService : uses
    ProjectService ..> FileDAO : calls
    ProjectService ..> UserDAO : calls
    ProjectService ..> AuditDAO : calls
    API ..> ProjectService : calls
    AuditService ..> AuditDAO : calls
    AuditService ..> FileDAO : calls
    API ..> AuditService : calls

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SBOMService : uses

    %% Colors

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
