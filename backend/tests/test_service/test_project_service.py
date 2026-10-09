from unittest.mock import MagicMock

from src.business_object.file.codefile import CodeFile
from src.business_object.file.dependencyfile import DependencyFile
from src.business_object.project import Project
from src.business_object.user import User
from src.dao.project_dao import ProjectDao
from src.service.project_service import ProjectService

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

project_list = [
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
    Project(
        id_project=4,
        name_project="salade_de_fruit",
        user=User(id_user=2, username="Clémentine", email="poire@pomme.fr", password="banane"),
        codefile=CodeFile(id_file=1, name="citron", path=""),
        dependencyfile=DependencyFile(id_file=2, name="myrtille", path="", dependencies=[]),
        secretHMACkey=bytes.fromhex(
            "7f55be633e93f7de0d8ac2ab8a3993fb7123c84f73582da121c2c62051596297"
        ),
    ),
    Project(
        id_project=5,
        name_project="derniere_minute",
        user=User(id_user=3, username="Gérard", email="gg@mail.fr", password="abcd"),
        secretHMACkey=bytes.fromhex(
            "3473cd7a6732d97355b5c8fa4e56420fad119fcf01d5255aa81a0cf576ccc912"
        ),
    ),
]

# En plus si besoin :
# bytes.fromhex("858470290e217b99b5bf2b6fdbaaeb43c8a903d87cd03de2705ca56ca8a3ce3e")
# codefile = CodeFile(id_file=3, name="le_fichier_code", path="")
#     dependencyfile = DependencyFile(
#         id_file=4, name="le_fichier_dependences", path="", dependencies=[]
#     )
# bytes.fromhex("822931904fd51a85179d0af5408dd461297be80066289afc08ad0980fd8fa755")
# codefile = CodeFile(id_file=5, name="fichier_1", path="")
#     dependencyfile = DependencyFile(id_file=6, name="fichier_2", path="", dependencies=[])


def test_upload_ok():
    """Successfully upload a Project"""

    # GIVEN
    name_project = "inspirations"
    user = User("Jean_Edouard", "je@mail.oo", password="tropical")
    ProjectDao().create = MagicMock(return_value=True)

    # WHEN
    project = ProjectService().upload(name_project, user)

    # THEN
    assert project.name_project == name_project


def test_upload_fail():
    """Fail to upload a Project because ProjectDao().create returns False"""

    # GIVEN
    id_project, name_project, secretHMACkey = "project_numero_512"
    user = User("Jean_Nemard", "jn@hotmail.nul", password="desert")
    ProjectDao().create = MagicMock(return_value=False)

    # WHEN
    project = ProjectService().upload(name_project, user)

    # THEN
    assert project is None


def test_list_all_project():
    """List all project of a user"""

    # GIVEN
    ProjectDao().list_all_project = MagicMock(return_value=project_list_michel)

    # WHEN
    res = ProjectService().list_all_project(1)

    # THEN
    assert len(res) == 3


# tests manquants : update_successful/failed, delete, find_by_id_successful/failed
