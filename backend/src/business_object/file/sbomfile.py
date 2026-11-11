from datetime import datetime

from business_object.file.file import File


class SBOMFile(File):
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

    def __init__(self, name, content, type_file, date) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.date = date if date is not None else datetime.now()

    # Method to move to utils, unless it differs from the CodeFile method
    # def get_content(self) -> bool:
    #     try:
    #         with open(self.path, encoding="utf-8") as file:
    #             self.content = file.read()
    #         return True
    #     except (FileNotFoundError, OSError):
    #         return False

    def get_duty(self) -> str:
        """
        Return the role of the file within a project

        Returns
        -------
        str
            Always sbom
        """
        return "sbom"
