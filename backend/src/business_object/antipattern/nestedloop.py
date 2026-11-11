from business_object.antipattern.antipattern import AntiPattern


class NestedLoop(AntiPattern):
    """
    Antipattern representing nested loops (for/while) beyond a minimum depth.

    Attributes
    ----------
    id_antipattern : int
        Unique identifier of the nested loop.
    line : int
        Line number where the nested loop was detected.
    description : str
        Description of the nested loop.
    depth : int
        Nesting depth of the loop.
    """

    def __init__(self, line, description, depth, id_antipattern: int | None = None) -> None:
        super().__init__(line, description, id_antipattern)
        self.depth = depth

    def __str__(self) -> str:
        """
        Return a readable representation of the nested loop.

        Returns
        -------
        str
            String showing the line and the depth of the loop.
        """
        return (
            f"[NestedLoop] line :{self.line}"
            + "\n"
            + f"boucle imbriquée de profondeur {self.depth}"
        )
