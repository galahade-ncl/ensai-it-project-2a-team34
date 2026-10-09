class Dependency:
    """
    Classe représentant une dépendance.

    Attributes
    ----------
    id_dependency : int
        Identifiant de la dépendance
    name : str
        Nom de la dépendance
    version : str
        Version de la dépendance
    """

    def __init__(self, id_dependency, name, version):
        self.id_dependency = id_dependency
        self.name = name
        self.version = version
