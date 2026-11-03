import hashlib
import hmac
import os
import uuid
from datetime import date
from io import BytesIO

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from business_object.audit import Audit
from business_object.file.certificatefile import CertificateFile
from business_object.project import Project
from utils.log_utils import log

# La clé doit venir de l'environnement / config, jamais du code
SECRET_KEY = os.environ["CERTIFICATE_SECRET_KEY"].encode()

# Un modèle par type de quality gate : adapte les clés à tes vraies valeurs
TEMPLATES = {
    "eco": {
        "title": "Certificat Éco",
        "color": colors.HexColor("#8c5a2b"),
        "text": "a satisfait les exigences ",
    },
    "security": {
        "title": "Certificat Sécurité",
        "color": colors.HexColor("#7a7a7a"),
        "text": "a satisfait aux exigences avancées du quality gate",
    },
    "global": {
        "title": "Certificat Global",
        "color": colors.HexColor("#b8860b"),
        "text": "has met all the requirements ",
    },
}


def sign(cert_id: str, project: str, qualitygate_type: str, issued: str) -> str:
    data = f"{cert_id}|{project}|{qualitygate_type}|{issued}"
    return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()[:24]


class CertificateService:
    @log
    def generate_certificate(
        self, audit: Audit, project: Project, qualitygate_type: str
    ) -> CertificateFile:
        if qualitygate_type not in TEMPLATES:
            raise ValueError(f"Type de certificat inconnu : {qualitygate_type}")

        tpl = TEMPLATES[qualitygate_type]
        cert_id = str(uuid.uuid4())
        issued = date.today().isoformat()
        project_name = project.name_project
        signature = sign(cert_id, project_name, qualitygate_type, issued)

        buffer = BytesIO()
        w, h = landscape(A4)
        c = canvas.Canvas(buffer, pagesize=(w, h))

        # Cadre + titre
        c.setStrokeColor(tpl["color"])
        c.setLineWidth(6)
        c.rect(30, 30, w - 60, h - 60)
        c.setFillColor(tpl["color"])
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(w / 2, h - 120, tpl["title"])

        # Corps
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 16)
        c.drawCentredString(w / 2, h - 190, "Il est certifié que le projet")
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(w / 2, h - 240, project_name)
        c.setFont("Helvetica", 16)
        c.drawCentredString(w / 2, h - 290, tpl["text"])
        c.drawCentredString(w / 2, h - 320, f"Délivré le {issued}")

        # Identifiant + signature
        c.setFont("Courier", 9)
        c.drawString(50, 60, f"ID : {cert_id}")
        c.drawString(50, 48, f"Signature : {signature}")

        # QR code (contient de quoi vérifier le certificat)
        payload = f"{cert_id}|{signature}"
        widget = qr.QrCodeWidget(payload)
        x0, y0, x1, y1 = widget.getBounds()
        size = 90
        d = Drawing(size, size, transform=[size / (x1 - x0), 0, 0, size / (y1 - y0), 0, 0])
        d.add(widget)
        renderPDF.draw(d, c, w - size - 50, 50)

        c.showPage()
        c.save()

        return CertificateFile(
            name="Certificate: " + qualitygate_type,
            content=buffer.getvalue(),
            type_file="pdf",
            qualitygate_type=qualitygate_type,
            date=issued
        )


# from business_object.audit import Audit
# from business_object.certificate import Certificate
# from utils.log_utils import log


# class CertificateService:
#     # PAS FINI
#     @log
#     def generate_certificate(self, audit: Audit, qualitygate_type: str) -> Certificate:
#         """Generate a certificate for a project during its audit
#         Args:
#             audit (Audit) : the audit of the project
#         Returns:
#             Certificate object linked to the project
#         """
#         return Certificate(
#             name="Certificate: " + qualitygate_type,
#             content=None,
#             type_file="pdf",
#             qualitygate_type=qualitygate_type,
#         )
