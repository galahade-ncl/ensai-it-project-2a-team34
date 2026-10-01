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

    Methods
    -------
    __str__ : str
        Retourne la représentation informelle d'un utilisateur
    __eq__ : bool
        Renvoie True si les utilisateurs comparés sont identiques
    __hash__ : int
        renvoie une version hashée de l'id de l'utilisateur. 
        (Permet l'usage d'un set ou d'un dict).
    """
    def __init__(self, id_user, username, passeword, email, access_token=None) -> None:
        self.id_user = id_user
        self.username = username
        self.passeword = passeword
        self.email = email
        self.access_token = access_token

    def __str__(self) -> str:
        return f"{self.username} (id :{self.id_user}, email : {self.email})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id_user == other.id_user

    def __hash__(self) -> int:
        return hash(self.id_user)
