from datetime import datetime

from business_object.file.file import File


class CertificateFile(File):
    """
    Certificate issued at the end of an audit.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the certificate (PDF) in bytes.
    type_file : str
        Extension of the file.
    qualitygate_type : str
        Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
    date : datetime
        Generation date of the certificate. Set to the current date if
        None is given.
    signed_data : dict
        Signed certificate data (``payload``, ``kid``, ``alg`` and
        ``signature``), as embedded in the QR code.
    """

    def __init__(self, name, content, type_file, qualitygate_type, date, signed_data) -> None:
        self.name = name
        self.content = content
        self.type_file = type_file
        self.qualitygate_type = qualitygate_type
        self.date = date if date is not None else datetime.now()
        self.signed_data = signed_data

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'certificate'`` for this class.
        """
        return "certificate"
