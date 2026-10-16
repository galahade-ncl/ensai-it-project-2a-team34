from business_object.file.file import File


class DependencyFile(File):
    """A compléter

    Attributes
    ----------
    name : str
        Nom du fichier
    content : bytes
        Contenu du fichier en format bytes
    date : datetime
        Date de dépot du fichier
    """

    def __init__(self, name, content, type_file, date=None) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.date = date
        # self.dependencies = dependencies -> retiré pour l'instant

    # Méthode a déplacer dans utils, sauf si différente de méthode de codefile
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        return "dependency"

    # Méthode à réfléchir : récup la liste des dépendencies
