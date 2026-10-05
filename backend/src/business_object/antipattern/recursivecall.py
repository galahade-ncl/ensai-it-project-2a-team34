from business_object.antipattern import AntiPattern


class RecursiveCall(AntiPattern):
    """Antipattern representing a direct recursive call: a function that calls itself by name

    Uncontrolled recursion can lead to high number of function callsand therefore to unnecessary energy consumption.


     Attributes:
            id_antipattern (int): The unique identifier of the recursive call
            line(int): The line number where the recursive call was detected
            description(str): The description of the recursive call
            function_name(str): Name of the function that calls itself

    """

    def __init__(self, line, description, function_name, id_pattern: int | None = None):
        super().__init__(line, description, id_pattern)
        self.function_name = function_name

    def __str__(self):
        """Readable representation of the recursive call.
        Returns: a str which shows the line and the name of the recursive function
        """
        return (
            f"[RecursiveCall] line :{self.line}"
            + "\n"
            + f"la fonction '{self.function_name}' s'appelle elle-même"
        )
