class Dependency:
    """
    Class representing a dependency.

    Attributes
    ----------
    id_dependency : int or None
        Unique identifier of the dependency.
    name : str
        Name of the dependency.
    version : str
        Version of the dependency.
    """

    def __init__(self, name, version, id_dependency=None) -> None:
        self.id_dependency = id_dependency
        self.name = name
        self.version = version
