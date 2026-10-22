from fastapi import APIRouter, Depends, HTTPException

from schema.audit_model import AuditCreateModel, AuditReadModel, AuditResponseModel
from service.audit_service import AuditService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_audit_service():
    """Dependency Injection provider for AuditService."""
    return AuditService()


@router.get("audits/{id_audit}", response_model=AuditReadModel, tags=["Audits"])
async def audit_by_id(id_audit: int, audit_service=Depends(get_audit_service)):
    """Find an audit by its unique ID.
    Args:
        id_audit (int)
        audit_service (AuditService): The service used to interact with audit data
    Returns:
        AuditRead: The audit data if found
    Raises:
        HTTPException: 404 error if the audit is not found
    """
    logger.info("Find an audit by id")
    audit = audit_service.find_by_id(id_audit)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit (id={id_audit}) not found.")
    return audit



@router.get("audits/{id_user}/audits", response_model=list[AuditReadModel], tags=["Audits"])
async def audit_by_audit(id_audit: int, audit_service=Depends(get_audit_service)):
    """
    Retrieve audits filtered by audit ID.
    """

    return audit_service.list_all_audit(id_audit)



@router.post("/audits", response_model=AuditResponseModel, tags=["Audits"])
async def create_audit(p: AuditCreateModel, audit_service=Depends(get_audit_service)):
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

    audit = AuditService().find_by_id(p.id_audit)

    audit = audit_service.run_audit(audit)

    if not audit:
        raise HTTPException(status_code=500, detail="Error while creating audit.")

    return audit

