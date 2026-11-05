import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException

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
    """Dependency Injection provider for AuditService."""
    return AuditService()


def get_project_service():
    """Dependency Injection provider for ProjectService."""
    return ProjectService()


@router.get("/{id_audit}", response_model=AuditReadModel, tags=["Audits"])
async def audit_by_id(id_audit: int, user=Depends(verify_token), audit_service=Depends(get_audit_service), project_service=Depends(get_project_service)):
    """Find an audit by its unique ID.
    Args:
        id_audit (int)
        audit_service (AuditService): The service used to interact with audit data
    Returns:
        AuditReadModel: The audit data if found
    Raises:
        HTTPException: 404 error if the audit is not found
    """
    logger.info("Find an audit by id")

    audit = audit_service.find_by_id(id_audit)

    project = project_service.find_by_id_and_user(audit.id_project, user.id_user)
    if not project:
        raise HTTPException(status_code=404, detail="Audit not found or you do not have access to it.")

    if not audit:
        raise HTTPException(status_code=404, detail="Audit (id={id_audit}) not found.")
    return audit


@router.post("/", response_model=AuditResponseModel, tags=["Audits"])
async def create_audit(
    p: AuditCreateModel,
    user=Depends(verify_token),
    audit_service=Depends(get_audit_service),
    project_service=Depends(get_project_service),
):
    """Create a new audit.
    Args:
        p (AuditCreateModel): The audit data to create.
        audit_service (AuditService): The service used to interact with audit data.
    Returns:
        AuditResponseModel: The newly created audit data.
    Raises:
        HTTPException: 500 error if the creation process fails.
    """
    logger.info("Create an audit")

    # Get the project
    project = project_service.find_by_id_and_user(id_project=p.project.id_project, id_user=user.id_user)

    if not project:
        raise HTTPException(status_code=404, detail="Audit not found or you do not have access to it.")

    # Decode the base64 received
    try:
        code_content = base64.b64decode(p.project.codefile.content)
        dep_content = base64.b64decode(p.project.dependencyfile.content)
    except Exception as e:
        logger.error(f"Base64 decoding error: {e}")
        raise HTTPException(status_code=400, detail="Invalid Base64 content in files.")

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
        raise HTTPException(status_code=400, detail="Invalid signature format")

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
