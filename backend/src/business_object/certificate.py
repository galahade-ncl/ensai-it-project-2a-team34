class Certificate:
    """
    Classe représentant un certificat.

    Attributes
    ----------
    id_certificate : int
        Identifiant du certificat
    date : datetime
        Date du certificat
    type : str
        Type du certificat
    status : str
        Statut du certificat
    path : str
        Chemin d'accès au certificat
    """

    def __init__(self, id_certificate, date, type, status, path):
        self.id_certificate = id_certificate
        self.date = date
        self.type = type
        self.status = status
        self.path = path
