"""
Sarah
"""


class File:
    """
    Classe modélisant un fichier fournit par l'utilisateur.

    Attributes
    ----------
    name : str
        Nom du fichier
    id_file : int
        Identifiant du fichier
    date : datetime
        Date de dépot du fichier
    path :str
        Chemin d'accès du fichier

    Methods
    -------
    __str__() : str
        Renvoie la représentation informelle d'un fichier.
    __eq__ : bool
        Renvoie True si les fichiers comparés sont identiques
    __hash__ : int
        renvoie une version hashée de l'id du fichier.
        (Permet l'usage d'un set ou d'un dict).
    get_content() : bool
        Méthode qui permet de récupérer le contenu du fichier
        et renvoie un booléen de confirmation si le fichier a bien été récupéré
    get_type() : str
        Méthode qui permet d'obtenir le type de fichier (fichier de dépendance ou fichier code)
    """
    def __init__(self, id_file, date, path, name) -> None:
        self.id_file = id_file
        self.name = name
        self.date = date
        self.path = path

    def __str__(self) -> str:
        return f"{self.name} (id :{self.id_file}, path : {self.path}, date : {self.date})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, File):
            return NotImplemented
        return self.id_file == other.id_file

    def __hash__(self) -> int:
        return hash(self.id_file)

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
