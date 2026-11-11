from abc import ABC, abstractmethod


class File(ABC):
    """
    Abstract class modelling a file provided by the user.

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

    Methods
    -------
    __str__()
        Return a string representation of the file.
    __eq__(other)
        Return True if the compared files are identical.
    __hash__()
        Return a hash of the file ID, allowing files to be used in a set or as dict keys.
    get_content()
        Retrieve the content of the file and return whether it succeeded.
    get_type()
        Return the type of the file (dependency file or code file).
    """

    def __str__(self) -> str:
        return f"{self.name} (date : {self.date})"

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, File):
    #         return NotImplemented
    #     return self.id_file == other.id_file

    # def __hash__(self) -> int:
    #     return hash(self.id_file)

    # def get_path(self) -> str:
    #     """
    #     Method for retrieving the path (until we figure out how to save the files)
    #     """
    #     return "to be completed"

    # @abstractmethod
    # def get_content(self) -> bool:
    #     """
    #     Retrieves the contents of the file.
    #     """
    #     pass

    @abstractmethod
    def get_duty(self) -> str:
        """
        Return the type of the file.

        Returns
        -------
        str
            Type of the file (dependency file or code file).
        """
        pass
