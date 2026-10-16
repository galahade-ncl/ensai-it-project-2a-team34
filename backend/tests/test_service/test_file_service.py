from datetime import datetime

# import pytest
# from unittest.mock import MagicMock
from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile

# from src.dao.file_dao import FileDao
# from src.service.file_service import FileService


# @pytest.fixture(autouse=True)
# def reset_dao_singleton():
#     yield
#     # Nettoyage après chaque test
#     FileDao._instances.clear()


# For the list_all_by_project test
file_list_project_michel = [
    CodeFile(
        name="Le code du projet",
        content=b"print('Hello World')\n",
        type_file="py",
        date=datetime(2026, 1, 5, 8, 15, 23),
    ),
    CodeFile(
        name="Le code optionel du projet",
        content=b"print('Hello World, aRe yoU Ok ?')\n",
        type_file="py",
        date=datetime(2026, 1, 11, 11, 47, 5),
    ),
    DependencyFile(
        name="Il faut bien un fichier de dépendance au moins",
        content=b"requests==2.32.3\npytest==8.3.3\n",
        type_file="txt",
        date=datetime(2026, 1, 18, 10, 42, 5),
    ),
]

# For the other tests
file_list = [
    CodeFile(
        name="citron",
        content=b"""def presser_citron():
    return "Jus de citron"

print(presser_citron())
""",
        type_file="py",
        date=datetime(2026, 2, 3, 14, 30, 12),
    ),
    DependencyFile(
        name="myrtille",
        content=b"""requests==2.32.3\npytest==8.3.3""",
        type_file="txt",
        date=datetime(2026, 2, 21, 9, 5, 47),
    ),
    CodeFile(
        name="sucre",
        content=b"""def ajouter_sucre(quantite):
    return f"Ajout de {quantite} grammes de sucre"

print(ajouter_sucre(10))
""",
        type_file="py",
        date=datetime(2026, 3, 12, 16, 22, 31),
    ),
    DependencyFile(
        name="casserole",
        content=b'{"dependencies": {"express": "^4.21.0"}}',
        type_file="json",
        date=datetime(2026, 3, 27, 11, 18, 54),
    ),
    CodeFile(
        name="le_fichier_code",
        content="function add(a, b) { return a + b; }\n",
        type_file="py",
        date=datetime(2026, 4, 8, 13, 45, 9),
    ),
    DependencyFile(
        name="le_fichier_dependences",
        content=b"""<project>
                        <modelVersion>4.0.0</modelVersion>
                        <groupId>com.example</groupId>
                        <artifactId>my-app</artifactId>
                        <version>1.0.0</version>
                    </project>
                    """,
        type_file="xml",
        date=datetime(2026, 4, 19, 7, 32, 16),
    ),
    CodeFile(
        name="fichier_1",
        content="def multiply(a, b):\n    return a * b\n",
        type_file="py",
        date=datetime(2026, 5, 6, 15, 10, 42),
    ),
    DependencyFile(
        name="fichier_2",
        content=b'[project]\nname = "my-app"\ndependencies = ["requests>=2.0"]\n',
        type_file="toml",
        date=datetime(2026, 5, 24, 12, 55, 28),
    ),
]


# manque get_content (je sais pas si on les garde cette méthode)
