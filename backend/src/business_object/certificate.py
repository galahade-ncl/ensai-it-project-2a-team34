class Certificate:
    """
    Class representing a certificate.

    Attributes
    ----------
    id_certificate : int
        Unique identifier of the certificate.
    date : datetime
        Date of the certificate.
    type : str
        Type of the certificate.
    status : str
        Status of the certificate.
    path : str
        Path to the certificate.
    """

    def __init__(self, id_certificate, date, type, status, path) -> None:
        self.id_certificate = id_certificate
        self.date = date
        self.type = type
        self.status = status
        self.path = path
