from business_object.antipattern.antipattern import AntiPattern


class RecursiveCall(AntiPattern):
    """
    Antipattern representing a direct recursive call: a function that calls itself by name.

    Uncontrolled recursion can lead to a high number of function calls
    and therefore to unnecessary energy consumption.

    Attributes
    ----------
    id_antipattern : int
        Unique identifier of the recursive call.
    line : int
        Line number where the recursive call was detected.
    description : str
        Description of the recursive call.
    function_name : str
        Name of the function that calls itself.
    """

    def __init__(self, line, description, function_name, id_antipattern: int | None = None) -> None:
        super().__init__(line, description, id_antipattern)
        self.function_name = function_name

    def __str__(self) -> str:
        """
        Return a readable representation of the recursive call.

        Returns
        -------
        str
            String showing the line and the name of the recursive function.
        """
        return (
            f"[RecursiveCall] line :{self.line}"
            + "\n"
            + f"la fonction '{self.function_name}' s'appelle elle-même"
        )
