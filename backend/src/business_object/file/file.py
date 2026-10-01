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
    """
    def __init__(self, id_file, date, path) -> None:
        self.id_file = id_file
        self.date = date
        self.path = path

    def get_content(self) -> bool:
        ...  # Regarder comment est envoyé le fichier et les modifs souhaitées par le groupe
