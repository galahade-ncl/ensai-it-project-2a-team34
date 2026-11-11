from abc import ABC, abstractmethod

from business_object.audit import Audit


class QualityGate(ABC):
    """
    Abstract base class for all available quality gates.

    Subclasses define the thresholds checked against an audit and the
    type of quality gate they implement (eco, security or global).

    Methods
    -------
    evaluate(audit)
        Evaluate the audit against the quality gate and return whether
        it is respected.
    get_type()
        Return the type of the quality gate (``'eco'``, ``'security'``
        or ``'global'``).
    """

    @abstractmethod
    def evaluate(self, audit: Audit) -> bool:
        """
        Evaluate the audit against the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit to evaluate.

        Returns
        -------
        bool
            True if the quality gate is respected, False otherwise.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
        """
        pass
