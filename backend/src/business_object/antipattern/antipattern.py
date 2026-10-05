from abc import ABC, abstractmethod


class AntiPattern(ABC):
    """Abstract Class representing all detected antipatterns found in a project
    Attributes:
        id_antipattern (int): The unique identifier of the antipattern
        type(str): The type of the antipattern
        line(int): The line number where the antipattern was detected
        description(str): The description of the antipattern
    """

    def __init__(self, line, description, id_antipattern: int | None = None):
        self.id_antipattern = id_antipattern
        self.line = line
        self.description = description

    @abstractmethod
    def __str__(self):
        """Returns a string representation of the audit"""
        pass
