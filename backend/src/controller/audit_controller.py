import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException, Response

from business_object.file.codefile import CodeFile
from business_object.file.dependencyfile import DependencyFile
from business_object.project import Project
from schema.audit_model import AuditCreateModel, AuditReadModel, AuditResponseModel
from service.audit_service import AuditService
from service.project_service import ProjectService
from utils.log_utils import get_logger
from utils.security import verify_token

router = APIRouter()

logger = get_logger(__name__)


def get_audit_service():
    """
    Dependency injection provider for AuditService.

    Returns
    -------
    AuditService
        Instance of the audit service.
    """
    return AuditService()


def get_project_service():
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    return ProjectService()


@router.get("/{id_audit}", response_model=AuditReadModel, tags=["Audits"])
async def audit_by_id(
    id_audit: int,
    user=Depends(verify_token),
    audit_service=Depends(get_audit_service),
    project_service=Depends(get_project_service),
):
    """
    Find an audit by its unique ID.

    Parameters
    ----------
    id_audit : int
        Unique identifier of the audit.
    user : User
        Authenticated user (injected by ``verify_token``).
    audit_service : AuditService
        Service used to interact with audit data.
    project_service : ProjectService
        Service used to check that the user owns the audited project.

    Returns
    -------
    AuditReadModel
        The audit data if found.

    Raises
    ------
    HTTPException
        404 error if the audit is not found or if the user does not own
        the project linked to the audit.
    """
    logger.info("Find an audit by id")

    audit = audit_service.find_by_id(id_audit)

    # We check the audit exist before working on it
    if not audit:
        raise HTTPException(status_code=404, detail=f"Audit (id={id_audit}) not found.")

    # Check if the user owns the project linked to the audit or not
    project = project_service.find_by_id_and_user(audit.id_project, user.id_user)
    if not project:
        raise HTTPException(
            status_code=404, detail="Audit not found or you do not have access to it."
        )

    return audit


@router.post("/", response_model=AuditResponseModel, tags=["Audits"])
async def create_audit(
    p: AuditCreateModel,
    user=Depends(verify_token),
    audit_service=Depends(get_audit_service),
    project_service=Depends(get_project_service),
):
    """
    Create and run a new audit on a project.

    Decodes the Base64 files sent by the client, verifies the HMAC
    signature of the request, then runs the audit.

    Parameters
    ----------
    p : AuditCreateModel
        Audit data to create (project files, quality gate type and
        HMAC signature).
    user : User
        Authenticated user (injected by ``verify_token``).
    audit_service : AuditService
        Service used to interact with audit data.
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    AuditResponseModel
        The newly created audit data.

    Raises
    ------
    HTTPException
        400 error if the files or the signature are not valid Base64.
    HTTPException
        401 error if the HMAC signature is invalid.
    HTTPException
        404 error if the project is not found or not owned by the user.
    HTTPException
        500 error if the creation process fails.
    """
    logger.info("Create an audit")

    # Get the project and check if the user owns it or not
    project = project_service.find_by_id_and_user(
        id_project=p.project.id_project, id_user=user.id_user
    )

    if not project:
        raise HTTPException(
            status_code=404, detail="Project not found or you do not have access to it."
        )

    # Decode the base64 received
    try:
        code_content = base64.b64decode(p.project.codefile.content)
        dep_content = base64.b64decode(p.project.dependencyfile.content)
    except Exception as e:
        logger.error(f"Base64 decoding error: {e}")
        raise HTTPException(status_code=400, detail="Invalid Base64 content in files.") from None

    # Update the project
    project = Project(
        id_project=project.id_project,
        name_project=project.name_project,
        secretHMACkey=project.secretHMACkey,
        codefile=CodeFile(
            name=p.project.codefile.name,
            content=code_content,
            type_file=p.project.codefile.type_file,
        ),
        dependencyfile=DependencyFile(
            name=p.project.dependencyfile.name,
            content=dep_content,
            type_file=p.project.dependencyfile.type_file,
        ),
    )

    # Check the signature before verify_signature
    try:
        signature_bytes = base64.b64decode(p.hmac_signature, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(status_code=400, detail="Invalid signature format") from None

    # Verify HMAC signature before the launch of the audit
    if not project_service.verify_signature(project=project, signature=signature_bytes):
        raise HTTPException(status_code=401, detail="Invalid signature.")

    # Run audit
    audit = audit_service.run_audit(project, p.qualitygate_type)

    if not audit:
        raise HTTPException(status_code=500, detail="Error while creating audit.")

    if audit.certificate and isinstance(audit.certificate.content, bytes):
        audit.certificate.content = base64.b64encode(audit.certificate.content).decode("utf-8")

    if audit.sbom and isinstance(audit.sbom.content, bytes):
        audit.sbom.content = base64.b64encode(audit.sbom.content).decode("utf-8")

    return audit


# @router.get("/{id_audit}/certificate", tags=["Audits"])
# async def audit_certificate(
#     id_audit: int,
#     user=Depends(verify_token),
#     audit_service=Depends(get_audit_service),
#     project_service=Depends(get_project_service),
# ):
#     audit = audit_service.find_by_id(id_audit)
#     if not audit or not project_service.find_by_id_and_user(audit.id_project, user.id_user):
#         raise HTTPException(
#             status_code=404, detail="Audit not found or you do not have access to it."
#         )
#     if not audit.certificate:
#         raise HTTPException(status_code=404, detail="No certificate for this audit.")
#     return Response(content=audit.certificate.content, media_type="application/pdf")


@router.get("/{id_audit}/certificate", tags=["Audits"])
async def audit_certificate(
    id_audit: int,
    user=Depends(verify_token),
    audit_service=Depends(get_audit_service),
    project_service=Depends(get_project_service),
):
    """
    Download the PDF certificate of an audit.

    Parameters
    ----------
    id_audit : int
        Unique identifier of the audit.
    user : User
        Authenticated user (injected by ``verify_token``).
    audit_service : AuditService
        Service used to interact with audit data.
    project_service : ProjectService
        Service used to check that the user owns the audited project.

    Returns
    -------
    Response
        PDF file of the certificate, sent as an attachment.

    Raises
    ------
    HTTPException
        404 error if the audit is not found, not owned by the user, or
        has no certificate.
    HTTPException
        500 error if the certificate content is invalid.
    """
    audit = audit_service.find_by_id(id_audit)

    if not audit or not project_service.find_by_id_and_user(audit.id_project, user.id_user):
        raise HTTPException(
            status_code=404, detail="Audit not found or you do not have access to it."
        )

    if not audit.certificate:
        raise HTTPException(status_code=404, detail="No certificate for this audit.")

    try:
        content = audit.certificate.content

        # Decode Base64 if content is stored as a string
        if isinstance(content, str):
            content = base64.b64decode(content, validate=True)

        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="certificate_{id_audit}.pdf"'},
        )

    except (binascii.Error, ValueError):
        raise HTTPException(status_code=500, detail="Invalid certificate content.") from None


@router.get("/{id_audit}/sbom", tags=["Audits"])
async def audit_sbom(
    id_audit: int,
    user=Depends(verify_token),
    audit_service=Depends(get_audit_service),
    project_service=Depends(get_project_service),
):
    """
    Download the SBOM of an audit.

    Parameters
    ----------
    id_audit : int
        Unique identifier of the audit.
    user : User
        Authenticated user (injected by ``verify_token``).
    audit_service : AuditService
        Service used to interact with audit data.
    project_service : ProjectService
        Service used to check that the user owns the audited project.

    Returns
    -------
    Response
        JSON file of the SBOM, sent as an attachment.

    Raises
    ------
    HTTPException
        404 error if the audit is not found, not owned by the user, or
        has no SBOM.
    """
    audit = audit_service.find_by_id(id_audit)

    if not audit or not project_service.find_by_id_and_user(audit.id_project, user.id_user):
        raise HTTPException(
            status_code=404, detail="Audit not found or you do not have access to it."
        )

    if not audit.sbom or not audit.sbom.content or audit.sbom.content == b"0":
        raise HTTPException(status_code=404, detail="No SBOM for this audit.")

    return Response(
        content=audit.sbom.content,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="sbom_{id_audit}.json"'},
    )
