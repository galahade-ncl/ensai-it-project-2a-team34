
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
    class File {
        +id_file: int
        +name_file: string
        +id_user: int
        +HMAC_key: hmac.HMAC
    }
    class Audit {
        +id_audit: int
        +file_id: int
        +dependency_file : int
        +vulnerability:
        +
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
        +list_all_files(User, bool=False): list[File]
        +delete(User): bool
        +update(User): User
        +login(str,str): User
        +username_already_used(str): bool
    }


    class FileService {
        +create(int, str, int, hmac.HMAC): File
        +correct_HMAC_key(File): bool
        +find_by_id(int): File
        +find_user(int) : User
        +list_all_audit(int) : list[Audit]
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

    class FileController {
        +file_by_id(int): File
        +create_file(FileModel): File
        +update_file(int, FileModel): str
        +delete_file(int): str
    }

    class AuditController {
        +audit_by_id(int): Audit
        +create_audit(AuditModel): Audit
        +delete_audit(int): str
    }

    %% Relationships
    User "1" ..> "0..*" File : owns
    File "1" ..> "0..*" Audit
    UserService ..> UserDAO : calls
    UserService ..> User : uses
    UserService ..> FileDAO : calls
    UserService ..> File : uses
    UserDAO ..> User : uses
    UserController ..> UserService : calls
    FileService ..> FileDAO : calls
    FileService ..> File : uses
    FileService ..> User : uses
    FileService ..> UserDAO : calls
    FileService ..> Audit : uses
    FileService ..> AuditDAO : calls
    FileDAO ..> File : uses
    FileController ..> FileService : calls
    AuditService ..> Audit : uses
    AuditService ..> AuditDAO : calls
    AuditService ..> File : uses
    AuditService ..> FileDAO : calls
    AuditDAO ..> Audit : uses
    AuditController ..> AuditService : calls
```
