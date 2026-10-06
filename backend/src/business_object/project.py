# from business_object.file.codefile import CodeFile
# from business_object.file.dependencyfile import DependencyFile

class Project:
    ''' Class representing a code project upload by a user
        Attributes:
            id_project (int): The unique identifier of the project
            name_project (str): Name of the project
            user (User): User that owns the project
            codefile (CodeFile): the code file of the project
            dependencyfile (DependencyFile): the dependency file of the project
            secretHMACkey (hmac.HMAC): The secretHMACkey associated with the project
    '''

    def __init__(
        self,
        name_project,
        user,
        codefile,
        dependencyfile,
        secretHMACkey,
        id_project=None
    ):
        """Constructor"""
        self.id_project = id_project
        self.name_project = name_project
        self.user = user
        self.codefile = codefile
        self.dependencyfile = dependencyfile
        self.secretHMACkey = secretHMACkey

    def __str__(self):
        """Returns a string representation of the project
        Returns:
            str: A string containing the main informations about the project
        """
        return "-----------------------------------" + "\n" + f"{self.name_project} owns by {self.user}" + "\n" + "-----------------------------------"
