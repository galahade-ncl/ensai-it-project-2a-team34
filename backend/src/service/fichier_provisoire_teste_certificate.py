import os

os.environ["CERTIFICATE_SECRET_KEY"] = "cle-de-test"
from types import SimpleNamespace

from service.certificate_service import CertificateService

audit = SimpleNamespace(project=SimpleNamespace(name="Mon Projet"))
cert = CertificateService().generate_certificate(audit, "global")

with open("test_gold.pdf", "wb") as f:
    f.write(cert.content)
