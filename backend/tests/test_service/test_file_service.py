from datetime import datetime
from unittest.mock import MagicMock

from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile
from src.dao.file_dao import FileDao
from src.service.file_service import FileService

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


# Vérifier que le nom du file est le même est suffisant ?
def test_upload_successful():
    """Successfully upload a File"""

    # GIVEN
    file_name, type, id_project = "bonjour", "dependency", 1
    FileDao().create = MagicMock(return_value=True)

    # WHEN
    file = FileService().upload(file_name, type, id_project)

    # THEN
    assert file.name == file_name


def test_upload_failed():
    """Fail to upload a File because FileDao().create returns False"""

    # GIVEN
    file_name, type, id_project = "au revoir", "code", 1
    FileDao().create = MagicMock(return_value=False)

    # WHEN
    file = FileService().upload(file_name, type, id_project)

    # THEN
    assert file is None


def test_find_by_id_successful():
    """Successfully found the File related to the id"""

    # GIVEN
    file = file_list[1]
    id_of_file = file.id_file

    FileDao().find_by_id = MagicMock(result=file)

    # WHEN
    file_found = FileService().find_by_id(id_of_file)

    # THEN
    assert id_of_file == file_found.id_file


def test_find_by_id_failed():
    """Fail to found the File related to the id because FileDao().find_by_id returns None"""

    # GIVEN
    file = file_list[2]
    id_of_file = file.id_file

    FileDao().find_by_id = MagicMock(result=None)

    # WHEN
    file_found = FileService().find_by_id(id_of_file)

    # THEN
    assert file_found is None


def test_find_all_by_project():
    """List all files in the project associated with the id"""

    # GIVEN
    FileDao().find_all_by_project = MagicMock(return_value=file_list_project_michel)

    # WHEN
    result = FileService().find_all_by_project(2)

    # THEN
    assert len(result) == 3


def test_update_successful():
    """Successfully update the name of an existing File"""

    # GIVEN
    file = file_list[3]

    updated_name = "sel"
    file.name = updated_name

    FileDao().update = MagicMock(return_value=file)

    # WHEN
    updated_file = FileDao().update(file)

    # THEN
    assert updated_file.name == updated_name


def test_update_failed():
    """Fail to update the name of an existing File because FileDao().update returns None"""

    # GIVEN
    file = file_list[4]

    updated_name = "poêle"
    file.name = updated_name

    FileDao().update = MagicMock(return_value=None)

    # WHEN
    updated_file = FileService().update(file)

    # THEN
    assert updated_file is None


def test_delete_successful():
    """Successfully delete an existing File"""

    # GIVEN
    file = file_list[5]
    FileDao().delete = MagicMock(return_value=True)

    # WHEN
    result = FileDao().delete(file)

    # THEN
    assert result


def test_delete_failed():
    """Fail to delete an existing File because FileDao().delete returns False"""

    # GIVEN
    file = file_list[6]
    FileDao().delete = MagicMock(return_value=False)

    # WHEN
    result = FileDao().delete(file)

    # THEN
    assert not result


# manque find_user, find_project et get_content (je sais pas si on les garde ces méthodes)
