from fastapi import APIRouter

from service.audit_service import AuditService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_audit_service():
    """Dependency Injection provider for AuditService."""
    return AuditService()
