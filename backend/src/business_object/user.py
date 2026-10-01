"""
Sarah
"""


class User:
    """
    Classe qui modélise un utilisateur.

    Attributes
    ----------
    id_user : int
        Numéro qui identifie de manière unique un utilisateur.

    username : string
        Nom de l'utilisateur.

    passeword : string
        Le mot de passe de l'utilisateur

    email : string
        Email de l'utilisateur

    access_token : string | None
        Token de l'utilisateur (optionnel)
    """
    def __init__(self, id_user, username, passeword, email, access_token=None) -> None:
        self.id_user = id_user
        self.username = username
        self.passeword = passeword
        self.email = email
        self.access_token = access_token

    def __str__(self) -> str:
        ...

    def eq(self, other) -> bool:
        ...
