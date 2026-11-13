from business_object.file.file import File


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

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'dependency'`` for this class.
        """
        return "dependency"
