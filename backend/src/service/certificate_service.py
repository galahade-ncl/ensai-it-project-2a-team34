from business_object.audit import Audit
from business_object.certificate import Certificate
from utils.log_utils import log


class CertificateService:
    # PAS FINI
    @log
    def generate_certificate(self, audit: Audit) -> Certificate:
        """Generate a certificate for a project during its audit
        Args:
            audit (Audit) : the audit of the project
        Returns:
            Certificate object linked to the project
        """
        return Certificate(
            # il nous faut une table Certificate, ou alors on attribut l'id de l'audit au certificat (solution choisie)
            id_certificate=audit.id_audit,
            date=audit.date,
            type=audit.quality_gate.get_type(),
            status=audit.quality_gate.status,
            # utilité de path ? bah c'est utile, mais va falloir avoir une méthode générale pour récupérer les path pour les fichiers et les certificats 👀
        )
