# from business_object.file.codefile import CodeFile
# from business_object.file.dependencyfile import DependencyFile


class Project:
    """
    Class representing a code project uploaded by a user.

    Attributes
    ----------
    id_project : int or None
        Unique identifier of the project.
    name_project : str
        Name of the project.
    codefile : CodeFile or None
        Code file of the project.
    dependencyfile : DependencyFile or None
        Dependency file of the project.
    secretHMACkey : hmac.HMAC
        Secret HMAC key associated with the project.

    Methods
    -------
    __str__()
        Return a string representation of the project.
    """

    def __init__(
        self,
        name_project,
        secretHMACkey,
        id_project=None,
        codefile=None,
        dependencyfile=None,
    ) -> None:
        """Constructor"""
        self.id_project = id_project
        self.name_project = name_project
        self.codefile = codefile
        self.dependencyfile = dependencyfile
        self.secretHMACkey = secretHMACkey

    def __str__(self):
        """
        Return a string representation of the project.

        Returns
        -------
        str
            String containing the name of the project, framed by separator lines.
        """
        return (
            "-----------------------------------"
            + "\n"
            + f"{self.name_project}"
            + "\n"
            + "-----------------------------------"
        )
