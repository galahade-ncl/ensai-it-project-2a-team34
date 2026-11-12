class Licence:
    """
    Class representing a licence used by a project dependency.

    Attributes
    ----------
    id_licence : int or None
        Unique identifier of the licence.
    name : str
        Name of the licence.
    risk_level : str
        Risk level associated with the licence.

    Methods
    -------
    __repr__()
        Return an unambiguous string representation of the licence.
    __eq__(other)
        Return True if the other object is a Licence with the same name.
    __hash__()
        Return a hash based on the name of the licence, allowing licences
        to be used in a set or as dict keys.
    """

    def __init__(
        self,
        name,
        risk_level,
        id_licence=None) -> None:
        self.id_licence = id_licence
        self.name = name
        self.risk_level = risk_level

    # def __str__(self):
    #     return f"Name: {self.name}" + "\n" + f"Risk level: {self.risk_level}"

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the licence.

        Returns
        -------
        str
            String showing the name and the risk level of the licence.
        """
        return f"Licence(name={self.name!r}, risk_level={self.risk_level!r})"

    def __eq__(self, other) -> bool:
        """
        Compare the licence with another object.

        Two licences are considered equal if they have the same name,
        regardless of their risk level or identifier.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if ``other`` is a Licence with the same name, False otherwise.
        """
        return isinstance(other, Licence) and self.name == other.name

    def __hash__(self) -> int:
        """
        Return a hash of the licence.

        The hash is based on the name only, which keeps it consistent
        with ``__eq__``.

        Returns
        -------
        int
            Hash value of the licence name.
        """
        return hash(self.name)
