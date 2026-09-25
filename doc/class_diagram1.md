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
    %% Data Access Objects
    class UserDAO {
        +create(User): bool
        +find_by_id(int): User
        +find_all(): list[User]
        +delete(User): bool
        +update(User): User
        +login(str,str): User
    }

    class ProjectDAO {
        +upload(Project): bool
        +find_by_id(int): Project
        +delete(Project): bool
    }

    class FileDAO {
        +create(File): bool
        +find_by_id(int): File
        +find_all(): list[File]
        +delete(File): bool
        +update(File): File
    }
    class AuditDAO {
        +create(Audit): bool
        +find_by_id(int): Audit
        +find_all(): list[Audit]
    }

    %% Service layer
    class UserService {
        +create(str,str,str): User
        +find_by_id(int): User
        +list_all_project(User, bool=False): list[Project]
        +delete(User): bool
        +update(User): User
        +login(str,str): User
        +username_already_used(str): bool
    }

    class ProjectService {
        +upload(int, string, User, CodeFile, DependencyFile, hmac.HMAC): Project
        +upload_dependency_file(int, datetime, str, list[str]): DependencyFile
        +upload_code_file(int, datetime, str, ast.Module): CodeFile
        +update(Project): Project
        +find_by_id(int): Project
        +list_all_audit(int) : list[Audit]
        +delete(Project): bool
        +verify_HMAC_key(Project): bool
        +run_audit(Project): Audit
    }

    class FileService {
        +create_file(int, datetime, str): File
        +find_by_id(int): File
        +find_user(int): User
        +find_project(int): Project
        +delete(File): bool
        +update(File): File
        +submit(): bool
    }

    class AuditService {
        +create(int, int, datetime, list[Vulnerability], list[License], list[AntiPattern], float, float, float, QualityGate): Audit
        +find_by_id(int): Audit
        +find_user(int): User
        +find_project(int): Project
        +run_audit(Project): Audit
    }

    class SecurityService {
        +parse_dependencies(DependencyFile): list[str]
        +find_vulnerabilities(DependencyFile): list[Vulnerability]
        +find_licenses(DependencyFile): list[License]
    }

    class EcoService {
        +parse_ast(CodeFile): ast.Module
        +detect_antipatterns(CodeFile): list[AntiPattern]
        +estimate_complexity(CodeFile): float
        +calculate_energy(CodeFile): float
        +calculate_carbon(float): float
    }

    class SBOMService {
        +generate(Project): SBOM
    }

    class QualityGateService {
        +evaluate(Audit): QualityGate
        +generate_certificate(Audit): str
    }

    %% Controllers
    %% namespace API {
    %%     class UserController {
    %%         +user_by_id(int): User
    %%         +create_user(UserModel): User
    %%         +update_user(int, UserModel): str
    %%         +delete_user(int): str
    %%     }

    %%     class ProjectController {
    %%         +file_by_id(int): Project
    %%         +create_project(ProjectModel): Project
    %%         +update_project(int, ProjectModel): str
    %%         +delete_project(int): str
    %%         +all_audit(Project): list[Audit]
    %%         +last_audit(Project): Audit
    %%         +create_audit(AuditModel): Audit
    %%     }
    %% }

    class API {
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        }

    %% Relationships
    UserService ..> UserDAO : calls
    UserService ..> FileDAO : calls
    API ..> UserService : calls
    ProjectService ..> ProjectDAO : calls
    ProjectService ..> FileService : uses
    ProjectService ..> FileDAO : calls
    ProjectService ..> UserDAO : calls
    ProjectService ..> AuditDAO : calls
    API ..> ProjectService : calls
    AuditService ..> AuditDAO : calls
    AuditService ..> FileDAO : calls
    ProjectService ..> AuditService : calls

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

    %% style API fill:#F3E5F5,stroke:#8E44AD
    %% style ProjectController fill:#F3E5F5,stroke:#8E44AD

    style API fill:#F3E5F5,stroke:#8E44AD,color:#000
```
