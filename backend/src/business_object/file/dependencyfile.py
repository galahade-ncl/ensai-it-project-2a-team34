from business_object.file.file import File


# UNDONE
class DependencyFile(File):
    """
    Dependency file submitted for audit.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the file in bytes.
    type_file : str
        Extension of the file.
    date : datetime or None
        Submission date of the file.
    """

    def __init__(self, name, content, type_file, date=None) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.date = date
        # self.dependencies = dependencies -> withdrawn for now

    # Move this method to “utils,” unless it differs from the method in the code file
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'dependency'`` for this class.
        """
        return "dependency"
