class Licence:
    """Class representing a licence used by a project dependency
    Attributes:
        id_licence (int): The unique identifier of the licence
        name (str): The name of the licence
        risk_level (str): The risk level associated with the licence
    """

    def __init__(
        self,
        name,
        risk_level,
        id_licence=None):
        self.id_licence = id_licence
        self.name = name
        self.risk_level = risk_level

    def __str__(self):
        return f"Name: {self.name}" + "\n" + f"Risk level: {self.risk_level}"
