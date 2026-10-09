from datetime import datetime
from unittest.mock import MagicMock

from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile
from src.business_object.project import Project
from src.business_object.user import User
from src.dao.project_dao import ProjectDao
from src.service.project_service import ProjectService

# For the list_all_project test
project_list_michel = [
    Project(
        id_project=1,
        name_project="project_numero_1",
        user=User(id_user=1, username="Jean-michel", email="jean-michel@mail.fr", password="0000"),
        secretHMACkey=bytes.fromhex(
            "7f2cd2cada12a1c7f6550f4b9aa3873776d6b0228b2d9c1596dcdf8eda301930"
        ),
    ),
    Project(
        id_project=2,
        name_project="project_numero_2",
        user=User(id_user=1, username="Jean-michel", email="jean-michel@mail.fr", password="0000"),
        secretHMACkey=bytes.fromhex(
            "36ae536d5635a5ed214da489269b91dc9b9d4b97db9c077bd66830b54208329d"
        ),
    ),
    Project(
        id_project=3,
        name_project="project_numero_3",
        user=User(id_user=1, username="Jean-michel", email="jean-michel@mail.fr", password="0000"),
        secretHMACkey=bytes.fromhex(
            "4712c1bd6f34b112bc4af1f4ed09ba7e6f3db902a38b84c0754845862046cee7"
        ),
    ),
]

# For the other tests
project_list = [
    Project(
        id_project=4,
        name_project="salade_de_fruit",
        user=User(id_user=2, username="Clémentine", email="poire@pomme.fr", password="banane"),
        codefile=CodeFile(id_file=1, name="citron", date=datetime(2026, 2, 3, 14, 30, 12), path=""),
        dependencyfile=DependencyFile(
            id_file=2,
            name="myrtille",
            date=datetime(2026, 2, 21, 9, 5, 47),
            path="",
            dependencies=[],
        ),
        secretHMACkey=bytes.fromhex(
            "7f55be633e93f7de0d8ac2ab8a3993fb7123c84f73582da121c2c62051596297"
        ),
    ),
    Project(
        id_project=5,
        name_project="compote",
        user=User(id_user=2, username="Clémentine", email="poire@pomme.fr", password="banane"),
        codefile=CodeFile(id_file=3, name="sucre", date=datetime(2026, 3, 12, 16, 22, 31), path=""),
        dependencyfile=DependencyFile(
            id_file=4,
            name="casserole",
            date=datetime(2026, 3, 27, 11, 18, 54),
            path="",
            dependencies=[],
        ),
        secretHMACkey=bytes.fromhex(
            "a63d3f3e91dd4a09906d89caa4ccf7f45862f9e2e3c1a30268585b078aec2fda"
        ),
    ),
    Project(
        id_project=6,
        name_project="derniere_minute",
        user=User(id_user=3, username="Gérard", email="gg@mail.fr", password="abcd"),
        secretHMACkey=bytes.fromhex(
            "3473cd7a6732d97355b5c8fa4e56420fad119fcf01d5255aa81a0cf576ccc912"
        ),
    ),
    Project(
        id_project=7,
        name_project="impressions",
        user=User("Jean_Edouard", "je@mail.oo", password="tropical"),
        codefile=CodeFile(
            id_file=5, name="le_fichier_code", date=datetime(2026, 4, 8, 13, 45, 9), path=""
        ),
        dependencyfile=DependencyFile(
            id_file=6,
            name="le_fichier_dependences",
            date=datetime(2026, 4, 19, 7, 32, 16),
            path="",
            dependencies=[],
        ),
        secretHMACkey=bytes.fromhex(
            "858470290e217b99b5bf2b6fdbaaeb43c8a903d87cd03de2705ca56ca8a3ce3e"
        ),
    ),
    Project(
        id_project=8,
        name_project="project_numero_1502",
        user=User("Jean_Nemard", "jn@hotmail.nul", password="desert"),
        codefile=CodeFile(
            id_file=7, name="fichier_1", date=datetime(2026, 5, 6, 15, 10, 42), path=""
        ),
        dependencyfile=DependencyFile(
            id_file=8,
            name="fichier_2",
            date=datetime(2026, 5, 24, 12, 55, 28),
            path="",
            dependencies=[],
        ),
        secretHMACkey=bytes.fromhex(
            "822931904fd51a85179d0af5408dd461297be80066289afc08ad0980fd8fa755"
        ),
    ),
]


# Vérifier que le nom du projet est le même est suffisant ?
def test_upload_successful():
    """Successfully upload a Project"""

    # GIVEN
    name_project = "inspirations"
    user = User("Jean_Edouard", "je@mail.oo", password="tropical")
    ProjectDao().create = MagicMock(return_value=True)

    # WHEN
    project = ProjectService().upload(name_project, user)

    # THEN
    assert project.name_project == name_project


def test_upload_failed():
    """Fail to upload a Project because ProjectDao().create returns False"""

    # GIVEN
    name_project = "project_numero_512"
    user = User("Jean_Nemard", "jn@hotmail.nul", password="desert")
    ProjectDao().create = MagicMock(return_value=False)

    # WHEN
    project = ProjectService().upload(name_project, user)

    # THEN
    assert project is None


def test_find_by_id_successful():
    """Successfully found the Project related to the id"""

    # GIVEN
    project = project_list[1]
    project_id = project.id_project

    ProjectDao().find_by_id = MagicMock(result=project)

    # WHEN
    project_found = ProjectService().find_by_id(project_id)

    # THEN
    assert project_id == project_found.id_project


def test_find_by_id_failed():
    """Fail to found the Project related to the id because ProjectDao().find_by_id returns None"""

    # GIVEN
    project = project_list[2]
    project_id = project.id_project

    ProjectDao().find_by_id = MagicMock(result=None)

    # WHEN
    project_found = ProjectService().find_by_id(project_id)

    # THEN
    assert project_found is None


def test_list_all_project():
    """List all project of a user"""

    # GIVEN
    ProjectDao().list_all_project = MagicMock(return_value=project_list_michel)

    # WHEN
    res = ProjectService().list_all_project(1)

    # THEN
    assert len(res) == 3


def test_update_successful():
    """Successfully update the name of an existing Project"""

    # GIVEN
    project = project_list[4]

    updated_name = "new_impressions"
    project.name_project = updated_name

    ProjectDao().update = MagicMock(return_value=project)

    # WHEN
    updated_project = ProjectService().update(project)

    # THEN
    assert updated_project.name_project == updated_name


def test_update_failed():
    """Fail to update the name of an existing Project because ProjectDao().update returns None"""

    # GIVEN
    project = project_list[5]

    updated_name = "project_numero_0"
    project.name_project = updated_name

    ProjectDao().update = MagicMock(return_value=None)

    # WHEN
    updated_project = ProjectService().update(project)

    # THEN
    assert updated_project is None


def test_delete_successful():
    """Successfully delete an existing Project"""

    # GIVEN
    project = project_list[2]
    ProjectDao().delete = MagicMock(return_value=True)

    # WHEN
    result = ProjectService().delete(project)

    # THEN
    assert result


def test_delete_failed():
    """Fail to delete an existing Project because ProjectDao().delete returns False"""

    # GIVEN
    project = project_list[3]
    ProjectDao().delete = MagicMock(return_value=False)

    # WHEN
    result = ProjectService().delete(project)

    # THEN
    assert not result
