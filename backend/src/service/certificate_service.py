import base64
import hashlib
import json
import uuid
from datetime import UTC, datetime
from io import BytesIO

from cryptography.exceptions import InvalidSignature
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
from utils.security import canonical_json, get_key_id, load_signing_key

# A template for each qualitygate
TEMPLATES = {
    "eco": {
        "title": "Energy Efficiency Certificate",
        "color": colors.HexColor("#8c5a2b"),
        "text": "is hereby certified as meeting the applicable energy efficiency standards.",
    },
    "security": {
        "title": "Security Certification",
        "color": colors.HexColor("#7a7a7a"),
        "text": "is hereby certified as meeting the applicable security standards.",
    },
    "global": {
        "title": "General Quality Certification",
        "color": colors.HexColor("#b8860b"),
        "text": "is hereby certified as meeting the applicable overall quality standards.",
    },
}


class CertificateService:
    @log
    def generate_certificate(
        self, audit: Audit, project: Project, qualitygate_type: str
    ) -> CertificateFile:
        """Generates a signed PDF certificate for an audited project.

        The PDF embeds a QR code containing the signed certificate
        (payload, kid, signature), so it can be verified without database access.
        """
        if qualitygate_type not in TEMPLATES:
            raise ValueError(f"Unknown Certification : {qualitygate_type}")

        tpl = TEMPLATES[qualitygate_type]
        issued_at = datetime.now(UTC)
        issued = issued_at.date().isoformat()
        project_name = project.name_project

        payload = {
            "cert_id": str(uuid.uuid4()),
            "audit_id": audit.id_audit,
            "project_id": project.id_project,
            "project_name": project_name,
            "qualitygate_type": qualitygate_type,
            "qualitygate_status": audit.quality_gate.status,
            "issued_at": issued_at.isoformat(timespec="seconds"),
            "files": {
                "code_sha256": hashlib.sha256(project.codefile.content).hexdigest(),
                "dependencies_sha256": hashlib.sha256(project.dependencyfile.content).hexdigest(),
            },
            "summary": {
                "vulnerabilities": len(audit.vulnerabilities),
                "carbon_emission_gco2e": f"{audit.carbon_emission_gco2e:.6f}",
                "energy_consumption_kwh": f"{audit.energy_consumption_kwh:.6f}",
            },
            "app_version": "1.0.0",
        }
        signed = self.sign_certificate(payload)

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
        c.drawCentredString(w / 2, h - 190, "The project known as")
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(w / 2, h - 240, project_name)
        c.setFont("Helvetica", 16)
        c.drawCentredString(w / 2, h - 290, tpl["text"])
        c.drawCentredString(w / 2, h - 320, f"Issued on {issued}")

        # Identifiants
        c.setFont("Courier", 9)
        c.drawString(50, 72, f"ID : {payload['cert_id']}")
        c.drawString(50, 60, f"Key ID : {signed['kid']}")
        c.drawString(50, 48, f"Signature : {signed['signature'][:32]}...")

        # QR code : certificat signé complet
        qr_content = json.dumps(signed, separators=(",", ":"), ensure_ascii=False)
        widget = qr.QrCodeWidget(qr_content)
        x0, y0, x1, y1 = widget.getBounds()
        size = 130
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
            date=issued,
            signed_data=signed,
        )

    @staticmethod
    def sign_certificate(payload: dict) -> dict:
        """Signs a certificate payload with the application's private key."""
        signature = load_signing_key().sign(canonical_json(payload))
        return {
            "payload": payload,
            "kid": get_key_id(),
            "alg": "Ed25519",
            "signature": base64.b64encode(signature).decode("ascii"),
        }

    @staticmethod
    def verify_certificate(certificate: dict) -> bool:
        """Checks a signed certificate against the application's public key."""
        try:
            if certificate["kid"] != get_key_id():
                return False
            load_signing_key().public_key().verify(
                base64.b64decode(certificate["signature"]),
                canonical_json(certificate["payload"]),
            )
            return True
        except (InvalidSignature, KeyError, TypeError, ValueError):
            return False

    # Temporaire
    # def create_empty_certificate(self):
    #     return CertificateFile(
    #         name="Empty", content=b"0", type_file="pdf", qualitygate_type="global", date=None
    #     )
