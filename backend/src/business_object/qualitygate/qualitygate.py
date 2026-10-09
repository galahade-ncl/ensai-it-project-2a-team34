from abc import ABC, abstractmethod

from business_object.audit import Audit


class QualityGate(ABC):
    """Abstract base class for all qualitygate available."""

    @abstractmethod
    def evaluate(self, audit: Audit) -> bool:
        """Analyse the audit and returns a Boolean object."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Récupère le type de qualitygate (eco, security or global).
        """
        pass
