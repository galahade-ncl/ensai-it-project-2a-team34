"""
Sarah
"""


class File:
    """
    Classe modélisant un fichier fournit par l'utilisateur.

    Attributes
    ----------
    id_file : int
        Identifiant du fichier
    date : datetime
        Date de dépot du fichier
    path :str
        Chemin d'accès du fichier

    Methods
    -------
    get_content() : bool
        Méthode qui permet de récupérer le contenu du fichier
        et renvoie un booléen de confirmation si le fichier a bien été récupéré
    get_type() : str
        Méthode qui permet d'obtenir le type de fichier (fichier de dépendance ou fichier code)
    """
    def __init__(self, id_file, date, path) -> None:
        self.id_file = id_file
        self.date = date
        self.path = path

    def get_content(self) -> bool:
        """
        Récupère le contenu du fichier.
        """
        pass

    def get_type(self) -> str:
        """
        Récupère le type de fichier (fichier de dépendance ou fichier code).
        """
        pass
