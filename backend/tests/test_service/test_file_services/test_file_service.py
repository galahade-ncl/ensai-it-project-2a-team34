from datetime import datetime

import pytest

# from unittest.mock import MagicMock
from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile
from src.service.file_services.file_service import FileService

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
    DependencyFile(
        name="requirements",
        content=b"requests==2.0",
        type_file="txt",
        date=datetime(2026, 6, 10, 8, 46, 54),
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


def test_get_filename_successful():
    # GIVEN
    dependencyfile = file_list[1]

    # WHEN
    filename = FileService().get_filename(dependencyfile)

    # THEN
    assert filename == "myrtille.txt"


def test_get_filename_strips_leading_dot():
    # GIVEN
    dependencyfile = DependencyFile(name="package", type_file=".json", content=b"")

    # WHEN
    filename = FileService().get_filename(dependencyfile)

    # THEN
    assert filename == "package.json"


def test_parse_dependencies_successful():
    # GIVEN
    dependencyfile = file_list[4]
    list_result = [("requests", "2.0")]

    # WHEN
    list_dep = FileService().parse_dependencies(dependencyfile)

    # THEN
    for i in range(len(list_dep)):
        assert list_dep[i].name == list_result[i][0]
        assert list_dep[i].version == list_result[i][1]


def test_parse_dependencies_failed():
    # GIVEN
    dependencyfile = DependencyFile(name="doc", type_file="pdf", content=b"")

    # THEN
    with pytest.raises(ValueError):
        FileService().parse_dependencies(dependencyfile)


# manque get_content (je sais pas si on les garde cette méthode), parse_ast
