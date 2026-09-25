class Licence:
    """Class representing a licence used by a project dependency
    Attributes:
        id_license (int): The unique identifier of the licence
        name (str): The name of the licence
        risk_level (str): The risk level associated with the licence
    """

    def __init__(
        self,
        name,
        risk_level,
        id_license=None):
        self.id_license = id_license
        self.name = name
        self.risk_level = risk_level

    def __str__(self):
        return f"Name: {self.name}" + "\n" + f"Risk level: {self.risk_level}"
