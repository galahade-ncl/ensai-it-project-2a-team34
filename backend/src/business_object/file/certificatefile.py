import datetime

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

    def __init__(self, name, content, type_file, qualitygate_type, date=datetime.now()) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.qualitygate_type = qualitygate_type
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
        """Return the role of the file within a project"""
        return "certificate"

    # Temporaire
    def create_empty_certificate():
        return CertificateFile(
            name="Empty", content=b"0", type_file="pdf", qualitygate_type="global"
        )
