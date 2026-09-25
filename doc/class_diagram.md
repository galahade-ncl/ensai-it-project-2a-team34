
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

    %% Data Access Objects
    class UserDAO {
        +create(User): bool
        +find_by_id(int): User
        +list_all(): list[User]
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
        +list_all(): list[File]
        +delete(File): bool
        +update(File): File
    }
    class AuditDAO {
        +create(Audit): bool
        +find_by_id(int): Audit
        +list_all(): list[Audit]
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
        }

    %% Relationships
    User "1" ..> "0..*" Project : owns
    Project "1" ..> "0..*" Audit : owns
    UserService ..> UserDAO : calls
    UserService ..> User : uses
    UserService ..> FileDAO : calls
    UserService ..> Project : uses
    UserDAO ..> User : uses
    API ..> UserService : calls
    FileService ..> File : uses
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
    ProjectService ..> AuditService : calls

    Project ..> DependencyFile : uses
    Project ..> CodeFile : uses
    DependencyFile ..> File : uses
    CodeFile ..> File : uses

    Audit ..> Vulnerability : uses
    Audit ..> License : uses
    Audit ..> AntiPattern : uses
    Audit ..> QualityGate : uses

    AuditService ..> SecurityService : uses
    AuditService ..> EcoService : uses
    AuditService ..> QualityGateService : uses
    AuditService ..> SBOMService : uses

    QualityGateService ..> QualityGate : uses
    QualityGateService ..> Audit : uses
    SBOMService ..> Project : uses
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
    style Vulnerability fill:#E3F0FF,stroke:#4A90E2
    style License fill:#E3F0FF,stroke:#4A90E2
    style AntiPattern fill:#E3F0FF,stroke:#4A90E2
    style SBOM fill:#E3F0FF,stroke:#4A90E2
    style QualityGate fill:#E3F0FF,stroke:#4A90E2

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
