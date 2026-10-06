from abc import ABC, abstractmethod

from business_object.audit import Audit


class QualityGate(ABC):
    """Abstract base class for all qualitygate available."""

    @abstractmethod
    def evaluate(self, audit: Audit) -> bool:
        """Analyse the audit and returns a QualityGate object."""
        pass
