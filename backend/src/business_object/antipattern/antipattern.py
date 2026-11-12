from abc import ABC, abstractmethod


class AntiPattern(ABC):
    """
    Abstract class representing an antipattern detected in a project.

    Attributes
    ----------
    id_antipattern : int
        Unique identifier of the antipattern.
    type : str
        Type of the antipattern.
    line : int
        Line number where the antipattern was detected.
    description : str
        Description of the antipattern.
    """

    def __init__(self, line, description, id_antipattern: int | None = None):
        self.id_antipattern = id_antipattern
        self.line = line
        self.description = description

    @abstractmethod
    def __str__(self):
        """
        Return a string representation of the audit.

        Returns
        -------
        str
            String representation of the audit.
        """
        pass
