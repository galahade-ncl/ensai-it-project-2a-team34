"""
Sarah
"""

from abc import ABC, abstractmethod


class File(ABC):
    """
    Classe modélisant un fichier fournit par l'utilisateur.

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

    def __str__(self) -> str:
        return f"{self.name} (id :{self.id_file}, path : {self.path}, date : {self.date})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, File):
            return NotImplemented
        return self.id_file == other.id_file

    def __hash__(self) -> int:
        return hash(self.id_file)

    def get_path(self) -> str:
        """
        Méthode pour récupérer le path (en attendant de savoir comment on enregistre les fichiers)
        """
        return "à compléter"

    @abstractmethod
    def get_content(self) -> bool:
        """
        Récupère le contenu du fichier.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Récupère le type de fichier (fichier de dépendance ou fichier code).
        """
        pass
