
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
        +file_id: int
        +vulnerability_list : list[]
        +score_de_risque_global : int
    }

    %% Data Access Objects
    class UserDAO {
        +create(User): bool
        +find_by_id(int): User
        +list_all(): list[User]
        +delete(User): bool
        +update(User): bool
        +login(str,str): User
    }


    class FileDAO {
        +create(File): bool
        +find_by_id(int): File
        +list_all(): list[File]
        +delete(File): bool
        +update(File): bool
        +login(str,str): File
    }
    class AuditDAO {
        +create(Audit); bool
        +
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
        +create(int, string, User, CodeFile, DependencyFile, hmac.HMAC): Project
        +create_dependency_file(int, datetime, str, list[str]): DependencyFile
        +create_code_file(int, datetime, str, ast.Module): CodeFile
        +correct_HMAC_key(Project): bool
        +find_by_id(int): Project
        +find_user(int) : User
        +list_all_audit(int) : list[Audit]
        +delete(File): bool
    }

    class FileService {
        +create_file(): File
        +find_by_id(int): File
        +find_user(int): User
        +find_project(int): Project
        +delete(File): bool
    }


    class AuditService {
        +create()
    }

    %% Controllers
    class UserController {
        +user_by_id(int): User
        +create_user(UserModel): User
        +update_user(int, UserModel): str
        +delete_user(int): str
    }

    class ProjectController {
        +file_by_id(int): File
        +create_project(ProjectModel): File
        +update_project(int, ProjectModel): str
        +delete_project(int): str
    }

    class AuditController {
        +audit_by_id(int): Audit
        +create_audit(AuditModel): Audit
        +delete_audit(int): str
    }

    %% Relationships
    User "1" ..> "0..*" Project : owns
    Project "1" ..> "0..*" Audit
    UserService ..> UserDAO : calls
    UserService ..> User : uses
    UserService ..> FileDAO : calls
    UserService ..> Project : uses
    UserDAO ..> User : uses
    UserController ..> UserService : calls
    FileService ..> File : uses
    ProjectService ..> Project : uses
    ProjectService ..> FileService : uses
    ProjectService ..> FileDAO : calls
    ProjectService ..> File : uses
    ProjectService ..> User : uses
    ProjectService ..> UserDAO : calls
    ProjectService ..> Audit : uses
    ProjectService ..> AuditDAO : calls
    FileDAO ..> File : uses
    ProjectController ..> ProjectService : calls
    AuditService ..> Audit : uses
    AuditService ..> AuditDAO : calls
    AuditService ..> File : uses
    AuditService ..> FileDAO : calls
    AuditDAO ..> Audit : uses
    AuditController ..> AuditService : calls

    Project ..> DependencyFile : uses
    Project ..> CodeFile : uses
    DependencyFile ..> File : uses
    CodeFile ..> File : uses
```
