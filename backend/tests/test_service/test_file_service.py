from datetime import datetime

# from unittest.mock import MagicMock
from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile

# from src.dao.file_dao import FileDao
# from src.service.file_service import FileService


@pytest.fixture(autouse=True)
def reset_dao_singleton():
    yield
    # Nettoyage après chaque test
    FileDao._instances.clear()


# For the list_all_by_project test
file_list_project_michel = [
    CodeFile(
        id_file=1,
        name="Le code du projet",
        date=datetime(2026, 1, 5, 8, 15, 23),
        path="chemin imaginaire",
    ),
    CodeFile(id_file=2, name="Le code optionel du projet", path="chemin imaginaire 2"),
    DependencyFile(
        id_file=3,
        name="Il faut bien un fichier de dépendance au moins",
        date=datetime(2026, 1, 18, 10, 42, 5),
        path="chemin imaginaire 3",
        dependencies=[],
    ),
]

# For the other tests
file_list = [
    CodeFile(id_file=4, name="citron", date=datetime(2026, 2, 3, 14, 30, 12), path=""),
    DependencyFile(
        id_file=5, name="myrtille", date=datetime(2026, 2, 21, 9, 5, 47), path="", dependencies=[]
    ),
    CodeFile(id_file=6, name="sucre", date=datetime(2026, 3, 12, 16, 22, 31), path=""),
    DependencyFile(
        id_file=7,
        name="casserole",
        date=datetime(2026, 3, 27, 11, 18, 54),
        path="",
        dependencies=[],
    ),
    CodeFile(id_file=8, name="le_fichier_code", date=datetime(2026, 4, 8, 13, 45, 9), path=""),
    DependencyFile(
        id_file=9,
        name="le_fichier_dependences",
        date=datetime(2026, 4, 19, 7, 32, 16),
        path="",
        dependencies=[],
    ),
    CodeFile(id_file=10, name="fichier_1", date=datetime(2026, 5, 6, 15, 10, 42), path=""),
    DependencyFile(
        id_file=11,
        name="fichier_2",
        date=datetime(2026, 5, 24, 12, 55, 28),
        path="",
        dependencies=[],
    ),
]


# manque get_content (je sais pas si on les garde cette méthode)
