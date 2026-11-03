from business_object.file.file import File


class SbomFile(File):
    """Software Bill of Materials (SBOM) of an audited project.


    Attributes
    ----------
    name : str
        Name of the file
    content : bytes
        Content of the SBOM in bytes
    type_file: str
        Format of the file (json)
    date : datetime
        Generation date of the SBOM
    """

    def __init__(self, name, content, type_file, date=None) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.date = date

    # Méthode a déplacer dans utils, sauf si différente de méthode de codefile
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        """Return the role of the file within a project

        Returns
        -------
        str
             Always sbom
        """
        return "sbom"

    # Méthode à réfléchir : récup la liste des dépendencies
