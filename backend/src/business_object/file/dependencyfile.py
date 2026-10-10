from business_object.file.file import File


class DependencyFile(File):
    """A compléter

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
    """

    def __init__(self, id_file, name, path, date=None, dependencies=None) -> None:
        self.id_file = id_file
        self.name = name
        self.date = date | None
        self.path = path
        self.dependencies = dependencies | []

    # Méthode à retravailler (je sais pas encore ce qu'on en fait) (on la garde pour l'instant)
    def get_content(self) -> bool:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                self.content = file.read()
            return True
        except (FileNotFoundError, OSError):
            return False

    def get_type(self) -> str:
        return "dependency"

    # Méthode à réfléchir : récup la liste des dépendencies
