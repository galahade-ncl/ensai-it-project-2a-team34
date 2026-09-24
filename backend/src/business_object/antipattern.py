class AntiPattern: 
    """ Class representing an antipattern found in a project 
        Attributes: 
            id_antipattern (int): The unique identifier of the antipattern 
            type(str): The type of the antipattern
            line(int): The line number where the antipattern was detected
            description(str): The description of the antipattern
    """
    
    def __init__(
        self,
        type,
        line,
        descrpition,
        id_antipattern=None):
        self.id_antipattern=id_antipattern
        self.type=type
        self.line=line
        self.description=descrpition

    def __str__(self):
        """Returns a string representation of the audit
        """
        return f"Type : {self.type}" + "\n" + f"Detected on line number : {self.line}"+ "\n" + f"Description : {self.description}"