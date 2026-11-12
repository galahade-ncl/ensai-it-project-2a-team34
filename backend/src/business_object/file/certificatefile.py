from datetime import datetime

from business_object.file.file import File


# UNDONE
class CertificateFile(File):
    """
    Certificate of a file.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the SBOM in bytes.
    type_file : str
        Extension of the file.
    qualitygate_type : str
        Type of the quality gate.
    date : datetime
        Generation date of the SBOM
    signed_data : A COMPLETER
    """

    def __init__(self, name, content, type_file, qualitygate_type, date, signed_data) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.qualitygate_type = qualitygate_type
        self.date = date if date is not None else datetime.now()
        self.signed_data = signed_data

    # Move this method to “utils,” unless it differs from the method in the code file
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'certificate'`` for this class.
        """
        return "certificate"
