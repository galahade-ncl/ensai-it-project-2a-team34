from business_object.antipattern import AntiPattern


class NestedLoop(AntiPattern):
    """
    Antipattern represented nested loops (for/while) beyond a minimum depth

    Attributes:
            id_antipattern (int): The unique identifier of the nested loop
            line(int): The line number where the nested loop was detected
            description(str): The description of the nested loop
            depth(int): Nesting depth of the loop

    """

    def __init__(self, line, description, depth, id_pattern: int | None = None):
        super().__init__(line, description, id_pattern)
        self.depth = depth

    def __str__(self):
        """Readable representation of the nested loop
        Returns: a str which shows the line and the depth of the loop
        """
        return (
            f"[NestedLoop] line :{self.line}"
            + "\n"
            + f"boucle imbriquée de profondeur {self.depth}"
        )
