from datetime import datetime

from business_object.file.file import File


# PAS FINI
class CertificateFile(File):
    """Certificate of a file


    Attributes
    ----------
    name : str
        Name of the file
    content : bytes
        Content of the SBOM in bytes
    type_file: str
        Extension of the file
    qualitygate_type : str
        type of the qualitygate
    date : datetime
        Generation date of the SBOM
    """

<<<<<<< HEAD
    def __init__(self, name, content, type_file, qualitygate_type, date=datetime.datetime.now()) -> None:
=======
    def __init__(self, name, content, type_file, qualitygate_type, date) -> None:
>>>>>>> 8b36e4fefd2350917b24952b5fae709a825b7c01
        self.name = name
        self.content = content
        self.type_file = type_file
        self.qualitygate_type = qualitygate_type
        self.date = date if date is not None else datetime.now()

    # Méthode a déplacer dans utils, sauf si différente de méthode de codefile
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        """Return the role of the file within a project"""
        return "certificate"
