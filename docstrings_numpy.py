# =============================================================================
#  DOCSTRINGS — Projet Info (CleanOps)
#  Format : NumPy. Langue : anglais.
#
#  Mode d'emploi :
#  - Chaque bloc commence par le chemin du fichier source.
#  - Seules les signatures et les docstrings sont reprises : les corps sont
#    remplacés par "..." -> copier la docstring sous la ligne "def"/"class"
#    correspondante dans le vrai fichier.
#  - Docstrings de __init__ omises : en style NumPy, les paramètres du
#    constructeur sont décrits dans la docstring de la classe (Attributes).
#
#  Légende des marqueurs :
#    (aucun)       docstring existante reprise telle quelle
#    [CONVERTED]   docstring existante convertie du style Google -> NumPy
#    [FIXED]       docstring existante corrigée (erreur de contenu)
#    [NEW]         docstring absente dans le code, rédigée
#
#  Sommaire :
#    PARTIE 1 — business_object/
#    PARTIE 2 — api/, controller/, main.py, dao/, schema/
#    PARTIE 3 — service/
#    PARTIE 4 — service/file_services/, utils/
#    PARTIE 5 — frontend/
#    PARTIE 6 — tests/
# =============================================================================


# =============================================================================
#  PARTIE 1 — business_object/
# =============================================================================


# -----------------------------------------------------------------------------
# business_object/antipattern/antipattern.py
# -----------------------------------------------------------------------------
class AntiPattern(ABC):
    """
    Abstract class representing an antipattern detected in a project.

    Attributes
    ----------
    id_antipattern : int or None
        Unique identifier of the antipattern.
    line : int
        Line number where the antipattern was detected.
    description : str
        Description of the antipattern.

    Methods
    -------
    __str__()
        Return a readable representation of the antipattern.
    """

    # [FIXED] the docstring talked about "audit" instead of "antipattern"
    def __str__(self):
        """
        Return a readable representation of the antipattern.

        Must be implemented by subclasses.

        Returns
        -------
        str
            String representation of the antipattern.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/antipattern/nestedloop.py
# -----------------------------------------------------------------------------
class NestedLoop(AntiPattern):
    """
    Antipattern representing nested loops (for/while) beyond a minimum depth.

    Attributes
    ----------
    id_antipattern : int or None
        Unique identifier of the nested loop.
    line : int
        Line number where the nested loop was detected.
    description : str
        Description of the nested loop.
    depth : int
        Nesting depth of the loop.
    """

    def __str__(self) -> str:
        """
        Return a readable representation of the nested loop.

        Returns
        -------
        str
            String showing the line and the depth of the loop.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/antipattern/recursivecall.py
# -----------------------------------------------------------------------------
class RecursiveCall(AntiPattern):
    """
    Antipattern representing a direct recursive call: a function that calls itself by name.

    Uncontrolled recursion can lead to a high number of function calls
    and therefore to unnecessary energy consumption.

    Attributes
    ----------
    id_antipattern : int or None
        Unique identifier of the recursive call.
    line : int
        Line number where the recursive call was detected.
    description : str
        Description of the recursive call.
    function_name : str
        Name of the function that calls itself.
    """

    def __str__(self) -> str:
        """
        Return a readable representation of the recursive call.

        Returns
        -------
        str
            String showing the line and the name of the recursive function.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/audit.py
# -----------------------------------------------------------------------------
class Audit:
    """
    Class representing the audit of a project.

    Attributes
    ----------
    id_audit : int or None
        Unique identifier of the audit.
    id_project : int
        Unique identifier of the project linked to this audit.
    date : datetime
        Date the audit was created.
    vulnerabilities : list of Vulnerability
        Vulnerabilities found in the dependencies of the project.
    licenses : list of Licence
        Licences used by the project.
    anti_patterns : list of AntiPattern
        Antipatterns found in the project.
    complexity : float
        Complexity of the code.
    energy_consumption_kwh : float
        Energy consumption of the code (kWh).
    carbon_emission_gco2e : float
        Carbon emission of the code (gCO2e).
    sbom : SBOMFile
        Software Bill of Materials, the inventory of components used
        by the project.
    quality_gate : QualityGate
        Quality gate associated with the project.
    certificate : CertificateFile or None
        Certificate associated with the audit.

    Methods
    -------
    __str__()
        Return a string representation of the audit.
    """

    def __str__(self):
        """
        Return a string representation of the audit.

        Returns
        -------
        str
            String showing the project identifier and the energy
            consumption of the audit.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/certificate.py
# -----------------------------------------------------------------------------
class Certificate:
    """
    Class representing a certificate.

    Attributes
    ----------
    id_certificate : int
        Unique identifier of the certificate.
    date : datetime
        Date of the certificate.
    type : str
        Type of the certificate.
    status : str
        Status of the certificate.
    path : str
        Path to the certificate.
    """


# -----------------------------------------------------------------------------
# business_object/dependency.py
# -----------------------------------------------------------------------------
class Dependency:
    """
    Class representing a dependency.

    Attributes
    ----------
    id_dependency : int or None
        Unique identifier of the dependency.
    name : str
        Name of the dependency.
    version : str
        Version of the dependency.
    """


# -----------------------------------------------------------------------------
# business_object/licence.py
# -----------------------------------------------------------------------------
class Licence:
    """
    Class representing a licence used by a project dependency.

    Attributes
    ----------
    id_licence : int or None
        Unique identifier of the licence.
    name : str
        Name of the licence.
    risk_level : str
        Risk level associated with the licence.

    Methods
    -------
    __repr__()
        Return an unambiguous string representation of the licence.
    __eq__(other)
        Return True if the other object is a Licence with the same name.
    __hash__()
        Return a hash based on the name of the licence, allowing licences
        to be used in a set or as dict keys.
    """

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the licence.

        Returns
        -------
        str
            String showing the name and the risk level of the licence.
        """
        ...

    def __eq__(self, other) -> bool:
        """
        Compare the licence with another object.

        Two licences are considered equal if they have the same name,
        regardless of their risk level or identifier.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if ``other`` is a Licence with the same name, False otherwise.
        """
        ...

    def __hash__(self) -> int:
        """
        Return a hash of the licence.

        The hash is based on the name only, which keeps it consistent
        with ``__eq__``.

        Returns
        -------
        int
            Hash value of the licence name.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/project.py
# -----------------------------------------------------------------------------
class Project:
    """
    Class representing a code project uploaded by a user.

    Attributes
    ----------
    id_project : int or None
        Unique identifier of the project.
    name_project : str
        Name of the project.
    codefile : CodeFile or None
        Code file of the project.
    dependencyfile : DependencyFile or None
        Dependency file of the project.
    secretHMACkey : bytes
        Secret HMAC key associated with the project.

    Methods
    -------
    __str__()
        Return a string representation of the project.
    """

    # [FIXED] remove the '"""Constructor"""' docstring of __init__:
    # with Numpy style, constructor parameters are documented in the class docstring.

    def __str__(self):
        """
        Return a string representation of the project.

        Returns
        -------
        str
            String containing the name of the project, framed by separator lines.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/user.py
# -----------------------------------------------------------------------------
class User:
    """
    Class modelling a user.

    Attributes
    ----------
    id_user : int or None
        Unique identifier of the user.
    username : str
        Name of the user.
    password : str
        Password of the user.
    email : str
        Email of the user.
    access_token : str or None
        Access token of the user (optional).

    Methods
    -------
    __str__()
        Return an informal string representation of the user.
    __eq__(other)
        Return True if the compared users have the same identifier.
    __hash__()
        Return a hash of the user identifier, allowing users to be used
        in a set or as dict keys.
    """

    def __str__(self) -> str:
        """
        Return an informal string representation of the user.

        Returns
        -------
        str
            String showing the username, the identifier and the email
            of the user.
        """
        ...

    def __eq__(self, other) -> bool:
        """
        Compare the user with another object.

        Two users are considered equal if they have the same identifier.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if ``other`` is a User with the same identifier, False
            otherwise. ``NotImplemented`` is returned if ``other`` is not
            a User.
        """
        ...

    def __hash__(self) -> int:
        """
        Return a hash of the user.

        The hash is based on the identifier only, which keeps it consistent
        with ``__eq__``.

        Returns
        -------
        int
            Hash value of the user identifier.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/file/file.py
# -----------------------------------------------------------------------------
class File(ABC):
    """
    Abstract class modelling a file provided by the user.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the file in bytes.
    type_file : str
        Extension of the file.
    date : datetime or None
        Submission date of the file.

    Methods
    -------
    __str__()
        Return a string representation of the file.
    get_duty()
        Return the role of the file within a project.
    """
    # [FIXED] the "Methods" section listed methods that no longer exist
    # (__eq__, __hash__, get_content, get_type).

    # [NEW]
    def __str__(self) -> str:
        """
        Return a string representation of the file.

        Returns
        -------
        str
            String showing the name and the submission date of the file.
        """
        ...

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Must be implemented by subclasses.

        Returns
        -------
        str
            Role of the file (``'code'``, ``'dependency'``, ``'sbom'``
            or ``'certificate'``).
        """
        ...


# -----------------------------------------------------------------------------
# business_object/file/codefile.py
# -----------------------------------------------------------------------------
class CodeFile(File):
    """
    Source code file submitted for audit.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the file in bytes.
    type_file : str
        Extension of the file.
    date : datetime or None
        Submission date of the file.
    """

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'code'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/file/dependencyfile.py
# -----------------------------------------------------------------------------
class DependencyFile(File):
    """
    Dependency file submitted for audit.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the file in bytes.
    type_file : str
        Extension of the file.
    date : datetime or None
        Submission date of the file.
    """

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'dependency'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/file/sbomfile.py
# -----------------------------------------------------------------------------
class SBOMFile(File):
    """
    Software Bill of Materials (SBOM) of an audited project.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the SBOM in bytes.
    type_file : str
        Format of the file (``'json'``).
    date : datetime
        Generation date of the SBOM. Set to the current date if None
        is given.
    """

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'sbom'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/file/certificatefile.py
# -----------------------------------------------------------------------------
class CertificateFile(File):
    """
    Certificate issued at the end of an audit.

    Attributes
    ----------
    name : str
        Name of the file.
    content : bytes
        Content of the certificate (PDF) in bytes.
    type_file : str
        Extension of the file.
    qualitygate_type : str
        Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
    date : datetime
        Generation date of the certificate. Set to the current date if
        None is given.
    signed_data : dict
        Signed certificate data (``payload``, ``kid``, ``alg`` and
        ``signature``), as embedded in the QR code.
    """
    # [FIXED] "A COMPLETER" for signed_data, and "Content of the SBOM".

    def get_duty(self) -> str:
        """
        Return the role of the file within a project.

        Returns
        -------
        str
            Role of the file, always ``'certificate'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/qualitygate/qualitygate.py
# -----------------------------------------------------------------------------
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
        ...

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
        """
        ...


# -----------------------------------------------------------------------------
# business_object/qualitygate/ecoqualitygate.py
# -----------------------------------------------------------------------------
class EcoQualityGate:
    """
    Class representing the eco quality gate expected for the audit of a project.

    Attributes
    ----------
    max_carbon_emission : float
        Maximum carbon emission tolerated for a project.
    max_energy_consumption : float
        Maximum energy consumption tolerated for a project.
    status : str
        Status of the quality gate.

    Methods
    -------
    evaluate(audit)
        Check whether the project stays within the ecological thresholds.
    get_type()
        Return the type of the quality gate, always ``'eco'``.
    """

    def evaluate(self, audit: Audit) -> bool:
        """
        Check whether the project stays within the ecological thresholds.

        Compares the carbon emission and the energy consumption of the
        audit with the maximum values tolerated by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit of the project.

        Returns
        -------
        bool
            True if the project does not exceed the thresholds.
        """
        ...

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'eco'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/qualitygate/securityqualitygate.py
# -----------------------------------------------------------------------------
class SecurityQualityGate:
    """
    Class representing the security quality gate expected for the audit of a project.

    Attributes
    ----------
    max_vulnerabilities : int
        Maximum number of vulnerabilities tolerated for a project.
    max_critical_vulnerabilities : int
        Maximum number of critical vulnerabilities tolerated for a project.
    status : str
        Status of the quality gate.

    Methods
    -------
    evaluate(audit)
        Check whether the project stays within the vulnerability threshold.
    get_type()
        Return the type of the quality gate, always ``'security'``.
    """

    def evaluate(self, audit: Audit) -> bool:
        """
        Check whether the project stays within the vulnerability threshold.

        Compares the number of vulnerabilities found in the audit with the
        maximum number tolerated by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit of the project.

        Returns
        -------
        bool
            True if the project does not exceed the threshold.
        """
        ...

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'security'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/qualitygate/globalqualitygate.py
# -----------------------------------------------------------------------------
class GlobalQualityGate(QualityGate):
    """
    Class representing the global quality gate expected for the audit of a project.

    Attributes
    ----------
    max_vulnerabilities : int
        Maximum number of vulnerabilities tolerated for a project.
    max_critical_vulnerabilities : int
        Maximum number of critical vulnerabilities tolerated for a project.
    max_carbon_emission : float
        Maximum carbon emission tolerated for a project.
    max_energy_consumption : float
        Maximum energy consumption tolerated for a project.
    status : str
        Status of the quality gate.

    Methods
    -------
    __str__()
        Return a string representation of the quality gate.
    evaluate(audit)
        Evaluate the audit against all the thresholds of the quality gate.
    get_type()
        Return the type of the quality gate, always ``'global'``.
    """

    def __str__(self) -> str:
        """
        Return a string representation of the quality gate.

        Returns
        -------
        str
            String containing the status and the details of the quality gate.
        """
        ...

    def evaluate(self, audit: Audit) -> bool:
        """
        Evaluate the audit against the quality gate.

        Checks the results of the audit against the thresholds defined
        by the quality gate.

        Parameters
        ----------
        audit : Audit
            Audit to evaluate.

        Returns
        -------
        bool
            True if the quality gate is respected, False otherwise.
        """
        ...

    def get_type(self) -> str:
        """
        Return the type of the quality gate.

        Returns
        -------
        str
            Type of the quality gate, always ``'global'`` for this class.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/qualitygate/qualitygatefactory.py
# -----------------------------------------------------------------------------
class QualityGateFactory:
    """
    Factory class to create the appropriate QualityGate instances
    based on a string identifier.

    Methods
    -------
    get_qualitygate(type_qualitygate, max_vulnerabilities, max_critical_vulnerabilities,
                    max_carbon_emission, max_energy_consumption, status)
        Return an instance of the QualityGate matching the requested type.
    """

    @staticmethod
    def get_qualitygate(type_qualitygate, max_vulnerabilities, max_critical_vulnerabilities,
                        max_carbon_emission, max_energy_consumption, status) -> QualityGate:
        """
        Return an instance of the requested type of quality gate.

        Parameters
        ----------
        type_qualitygate : str
            Type of the quality gate expected (``'eco'``, ``'security'``
            or ``'global'``). The value is case-insensitive.
        max_vulnerabilities : int
            Maximum number of vulnerabilities tolerated for a project.
        max_critical_vulnerabilities : int
            Maximum number of critical vulnerabilities tolerated for a project.
        max_carbon_emission : float
            Maximum carbon emission tolerated for a project.
        max_energy_consumption : float
            Maximum energy consumption tolerated for a project.
        status : str
            Status of the quality gate.

        Returns
        -------
        QualityGate
            Instance of a class implementing QualityGate.

        Raises
        ------
        ValueError
            If the requested type is not supported.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/vulnerability/vulnerability.py
# -----------------------------------------------------------------------------
class Vulnerability(ABC):
    """
    Abstract base class for all vulnerabilities, with different severity levels.

    Attributes
    ----------
    id_vulnerability : int or None
        Unique identifier of the vulnerability.
    osv_id : str
        Identifier given by the external API, OSV.
    cve_id : str or None
        Identifier of the publicly disclosed vulnerability (CVE).
    package : str
        Package to which the vulnerability applies.
    version_package : str
        Version(s) of the package affected by the vulnerability.

    Methods
    -------
    __str__()
        Return a readable representation of the vulnerability.
    """

    def __str__(self):
        """
        Return a readable representation of the vulnerability.

        Returns
        -------
        str
            String describing the vulnerability. Must be implemented by
            subclasses.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/vulnerability/low_vulnerability.py
# -----------------------------------------------------------------------------
class LowVulnerability(Vulnerability):
    """
    Class representing a vulnerability of low severity.

    Methods
    -------
    __str__()
        Return a readable representation of the low severity vulnerability.
    """

    def __str__(self) -> str:
        """
        Return a readable representation of the low severity vulnerability.

        Returns
        -------
        str
            String showing the affected package and its version.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/vulnerability/medium_vulnerability.py
# -----------------------------------------------------------------------------
class MediumVulnerability(Vulnerability):
    """
    Class representing a vulnerability of medium severity.

    Methods
    -------
    __str__()
        Return a readable representation of the medium severity vulnerability.
    """
    # [FIXED] "high" -> "medium" in the Methods section

    def __str__(self) -> str:
        """
        Return a readable representation of the medium severity vulnerability.

        Returns
        -------
        str
            String showing the affected package and its version.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/vulnerability/high_vulnerability.py
# -----------------------------------------------------------------------------
class HighVulnerability(Vulnerability):
    """
    Class representing a vulnerability of high severity.

    Methods
    -------
    __str__()
        Return a readable representation of the high severity vulnerability.
    """

    def __str__(self) -> str:
        """
        Return a readable representation of the high severity vulnerability.

        Returns
        -------
        str
            String showing the affected package and its version.
        """
        ...


# -----------------------------------------------------------------------------
# business_object/vulnerability/critical_vulnerability.py
# -----------------------------------------------------------------------------
class CriticalVulnerability(Vulnerability):
    """
    Class representing a vulnerability of critical severity.

    Methods
    -------
    __str__()
        Return a readable representation of the critical vulnerability.
    """

    def __str__(self) -> str:
        """
        Return a readable representation of the critical vulnerability.

        Returns
        -------
        str
            String showing the affected package and its version.
        """
        ...


# =============================================================================
#  PARTIE 2 — api/, controller/, main.py, dao/, schema/
# =============================================================================


# -----------------------------------------------------------------------------
# api/api_deps_dev.py
# -----------------------------------------------------------------------------
class API_DEPSDEV:
    """
    Class that handles calls to the deps.dev API.

    Methods
    -------
    clean_version(version)
        Extract an exact version number from a version specifier.
    find_licences(dependency, ecosystem)
        Find the licences of a dependency.
    """

    @staticmethod
    def clean_version(version: str | None) -> str | None:
        """
        Extract an exact version number from a version specifier.

        Strips range operators and constraints (e.g. ``^``, ``>=``, ``<``)
        and keeps only the first version number found.

        Parameters
        ----------
        version : str or None
            Version specifier to clean (e.g. ``'^1.2.0'`` or ``'>=1.0,<2'``).

        Returns
        -------
        str or None
            The extracted exact version (e.g. ``'1.2.0'`` or ``'1.0'``),
            or None if no version can be extracted.

        Examples
        --------
        >>> API_DEPSDEV.clean_version('^1.2.0')
        '1.2.0'
        >>> API_DEPSDEV.clean_version('>=1.0,<2')
        '1.0'
        """
        ...

    # [FIXED] return type (list of Licence, not list of str) + Raises section
    @staticmethod
    def find_licences(dependency: Dependency, ecosystem: str) -> list[Licence]:
        """
        Find the licences of a dependency.

        Queries the deps.dev API for the given dependency and returns
        its licences with their risk level.

        Parameters
        ----------
        dependency : Dependency
            Dependency to look up.
        ecosystem : str
            OSV ecosystem name (e.g. ``'PyPI'``).

        Returns
        -------
        list of Licence
            Licences of the dependency. The list is empty if the
            dependency is unknown to deps.dev.

        Raises
        ------
        ValueError
            If the ecosystem is not supported by deps.dev.
        requests.HTTPError
            If the deps.dev API returns an error other than 404.
        """
        ...

    @staticmethod
    def _default_version(base: str) -> str | None:
        """
        Get the default version of a package.

        Used as a fallback when the dependency file does not specify
        any version for the package.

        Parameters
        ----------
        base : str
            Base URL used to query the package information.

        Returns
        -------
        str or None
            The default version of the package, or None if it cannot
            be determined.
        """
        ...

    @staticmethod
    def _to_licences(names: list[str]) -> list[Licence]:
        """
        Convert licence names into Licence objects.

        Maps each SPDX identifier returned by deps.dev to a Licence object
        and assigns it a risk level based on LICENCE_RISK.

        Parameters
        ----------
        names : list of str
            Licence names (SPDX identifiers) returned by deps.dev.

        Returns
        -------
        list of Licence
            Licence objects with their risk level. The risk level is
            ``'unknown'`` if the licence is not in LICENCE_RISK.
        """
        ...


# -----------------------------------------------------------------------------
# api/api_osv.py
# -----------------------------------------------------------------------------
class API_OSV:
    """
    Class that handles all the calls of the external API OSV.

    Attributes
    ----------
    BASE_URL : str
        URL of the OSV query endpoint.

    Methods
    -------
    find_vulnerabilities(dependency, ecosystem)
        Find all the vulnerabilities linked to a dependency.
    """

    @staticmethod
    def find_vulnerabilities(dependency: Dependency, ecosystem: str) -> list[Vulnerability]:
        """
        Find all the vulnerabilities linked to a dependency.

        Queries the OSV API for the given dependency and returns
        the vulnerabilities (CVE) that affect it.

        Parameters
        ----------
        dependency : Dependency
            Dependency to analyse through the external API.
        ecosystem : str
            Ecosystem associated with the dependency file (e.g. ``'PyPI'``).

        Returns
        -------
        list of Vulnerability
            Vulnerabilities linked to the dependency. The list is empty
            if none are found.

        Raises
        ------
        requests.HTTPError
            If the OSV API returns an error status code.
        """
        ...

    @staticmethod
    def _get_severity(osv_vuln: dict) -> str | None:
        """
        Determine the severity of a vulnerability from its CVSS vector.

        Reads the CVSS data (v2, v3 or v4) of an OSV vulnerability entry
        and converts its score into a severity level.

        Parameters
        ----------
        osv_vuln : dict
            Vulnerability entry returned by the OSV API.

        Returns
        -------
        str or None
            Severity level of the vulnerability (``'LOW'``, ``'MEDIUM'``,
            ``'HIGH'`` or ``'CRITICAL'``), or None if the vulnerability
            does not represent a risk or has no readable CVSS vector.
        """
        ...

    @staticmethod
    def _to_vulnerability(osv_vuln: dict, dependency: Dependency, severity: str) -> Vulnerability:
        """
        Transform an OSV API response into a Vulnerability object.

        Builds a Vulnerability from the raw entry returned by the OSV API,
        and links it to the analysed dependency with its severity level.

        Parameters
        ----------
        osv_vuln : dict
            Vulnerability entry returned by the OSV API.
        dependency : Dependency
            Dependency affected by the vulnerability.
        severity : str
            Severity level of the vulnerability.

        Returns
        -------
        Vulnerability
            Vulnerability subclass instance (Low, Medium, High or Critical)
            corresponding to the API entry.
        """
        ...


# -----------------------------------------------------------------------------
# controller/audit_controller.py
# -----------------------------------------------------------------------------
# [CONVERTED] Google style -> Numpy style

def get_audit_service():
    """
    Dependency injection provider for AuditService.

    Returns
    -------
    AuditService
        Instance of the audit service.
    """
    ...


def get_project_service():
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    ...


async def audit_by_id(id_audit, user, audit_service, project_service):
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
    ...


async def create_audit(p, user, audit_service, project_service):
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
    ...


# [NEW]
async def audit_certificate(id_audit, user, audit_service, project_service):
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
    ...


# [NEW]
async def audit_sbom(id_audit, user, audit_service, project_service):
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
    ...


# -----------------------------------------------------------------------------
# controller/certificate_controller.py
# -----------------------------------------------------------------------------

# [NEW]
def get_public_key():
    """
    Expose the public key used to sign the certificates.

    Returns
    -------
    dict
        Dictionary containing the key identifier (``kid``), the signing
        algorithm (``alg``) and the public key in PEM format
        (``public_key``).
    """
    ...


# [NEW]
def verify_certificate(cert):
    """
    Verify the signature of a certificate.

    Parameters
    ----------
    cert : SignedCertificateModel
        Signed certificate to verify (content of the QR code).

    Returns
    -------
    CertificateVerifyResponseModel
        Result of the verification: ``valid=True`` with the payload if
        the signature is correct, ``valid=False`` with a reason otherwise.
    """
    ...


# -----------------------------------------------------------------------------
# controller/hmac_controller.py
# -----------------------------------------------------------------------------

# [NEW]
async def create_hmac_signature(secret, project_id, code, dependency):
    """
    Generate the HMAC signature of a project submission.

    Parameters
    ----------
    secret : str
        Secret HMAC key of the project, encoded in Base64.
    project_id : int
        Unique identifier of the project.
    code : str
        Content of the code file, encoded in Base64.
    dependency : str
        Content of the dependency file, encoded in Base64.

    Returns
    -------
    dict
        Dictionary containing the signature encoded in Base64
        (``signature``).
    """
    ...


# -----------------------------------------------------------------------------
# controller/login_controller.py
# -----------------------------------------------------------------------------
# [CONVERTED]

def get_user_service():
    """
    Dependency injection provider for UserService.

    Returns
    -------
    UserService
        Instance of the user service.
    """
    ...


def login(credentials, service):
    """
    Authenticate a user.

    Parameters
    ----------
    credentials : UserLoginModel
        Username and password of the user.
    service : UserService
        Service used to interact with user data.

    Returns
    -------
    dict
        Dictionary containing ``id_user``, ``username`` and
        ``access_token``.

    Raises
    ------
    HTTPException
        401 error if the credentials are invalid or the user does not exist.
    """
    ...


# -----------------------------------------------------------------------------
# controller/project_controller.py
# -----------------------------------------------------------------------------
# [CONVERTED]

def get_project_service():
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    ...


async def project_by_id(id_project, user, project_service):
    """
    Find a project by its unique ID.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectReadModel
        The project data if found.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    """
    ...


async def create_project(p, user, project_service):
    """
    Create a new project.

    Parameters
    ----------
    p : ProjectCreateModel
        Project data to create.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectResponseModel
        The newly created project, with its secret HMAC key encoded
        in Base64.

    Raises
    ------
    HTTPException
        500 error if the creation process fails.
    """
    ...


async def delete_project(id_project, user, project_service):
    """
    Delete a project from the system.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    str
        Confirmation message indicating the project was deleted.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    """
    ...


async def update_project(id_project, p, user, project_service):
    """
    Update an existing project's information.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    p : ProjectCreateModel
        New data for the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    ProjectReadModel
        The updated project data.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    HTTPException
        500 error if the update process fails.
    """
    ...


async def regenerate_secret_key(id_project, user, project_service):
    """
    Generate a new secret key for a project.

    The old key stops working.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    dict
        Dictionary containing ``id_project``, ``name_project`` and the
        new ``secretHMACkey``.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    HTTPException
        500 error if the key could not be regenerated.
    """
    ...


async def audit_by_project(id_project, user, project_service):
    """
    Retrieve the audits of a project.

    Parameters
    ----------
    id_project : int
        Unique identifier of the project.
    user : User
        Authenticated user (injected by ``verify_token``).
    project_service : ProjectService
        Service used to interact with project data.

    Returns
    -------
    list of AuditReadModel
        Audits of the project.

    Raises
    ------
    HTTPException
        404 error if the project is not found or not owned by the user.
    """
    ...


# -----------------------------------------------------------------------------
# controller/user_controller.py
# -----------------------------------------------------------------------------
# [CONVERTED]

def get_user_service():
    """
    Dependency injection provider for UserService.

    Returns
    -------
    UserService
        Instance of the user service.
    """
    ...


def get_project_service():
    """
    Dependency injection provider for ProjectService.

    Returns
    -------
    ProjectService
        Instance of the project service.
    """
    ...


async def create_user(u, user_service):
    """
    Create a new user.

    Parameters
    ----------
    u : UserModel
        User data to create.
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    UserReadModel
        The newly created user data.

    Raises
    ------
    HTTPException
        400 error if the username is already taken.
    HTTPException
        500 error if the creation process fails.
    """
    ...


async def update_user(u, user, user_service):
    """
    Update the information of the authenticated user.

    Parameters
    ----------
    u : UserResponseModel
        New data for the user.
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    UserReadModel
        The updated user data.

    Raises
    ------
    HTTPException
        400 error if the new username is already taken.
    HTTPException
        404 error if the user is not found.
    HTTPException
        500 error if the update process fails.
    """
    ...


async def delete_user(user, user_service, project_service):
    """
    Delete the authenticated user and all their projects.

    Parameters
    ----------
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.
    project_service : ProjectService
        Service used to delete the projects of the user.

    Returns
    -------
    str
        Confirmation message indicating the user was deleted.

    Raises
    ------
    HTTPException
        404 error if the user is not found.
    """
    ...


async def project_by_user(user, user_service):
    """
    Retrieve the projects of the authenticated user.

    Parameters
    ----------
    user : User
        Authenticated user (injected by ``verify_token``).
    user_service : UserService
        Service used to interact with user data.

    Returns
    -------
    list of ProjectReadModel
        Projects owned by the user.
    """
    ...


# -----------------------------------------------------------------------------
# main.py
# -----------------------------------------------------------------------------
"""
Main entry point for the FastAPI web service.

Initializes logging, loads environment variables, and sets up API routers
for users, projects, audits and certificates.
"""


async def validation_exception_handler(request, exc):
    """
    Intercept Pydantic validation errors to log them.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.
    exc : RequestValidationError
        Validation error raised by FastAPI.

    Returns
    -------
    JSONResponse
        400 response containing the validation errors and the request body.
    """
    ...


async def redirect_to_docs():
    """
    Redirect to the API documentation.

    Returns
    -------
    RedirectResponse
        Redirection to ``/docs``.
    """
    ...


async def hello_name(name):
    """
    Display a hello message.

    Parameters
    ----------
    name : str
        Name to greet.

    Returns
    -------
    dict
        Dictionary containing the message.
    """
    ...


async def reset_database():
    """
    Reset the database.

    Returns
    -------
    dict
        Dictionary containing a message indicating whether the reset
        succeeded.
    """
    ...


# -----------------------------------------------------------------------------
# dao/db_connection.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class DBConnection(metaclass=Singleton):
    """
    Database connection manager implementing the Singleton pattern.

    This class ensures that only a single connection to the PostgreSQL
    database is opened and shared throughout the application lifecycle.

    Attributes
    ----------
    connection : psycopg2.extensions.connection
        The active database connection instance.

    Raises
    ------
    KeyError
        If any of the required ``POSTGRES_*`` environment variables are missing.
    psycopg2.Error
        If the connection to the database fails.
    """

    @property
    def connection(self):
        """
        Provide access to the underlying database connection.

        Returns
        -------
        psycopg2.extensions.connection
            The established database connection.
        """
        ...


# -----------------------------------------------------------------------------
# dao/user_dao.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class UserDao(metaclass=Singleton):
    """
    Class containing methods to access Users in the database.
    """

    def create(self, user) -> bool:
        """
        Create a user in the database.

        The identifier generated by the database is set on ``user``.

        Parameters
        ----------
        user : User
            User to create.

        Returns
        -------
        bool
            True if creation is successful, False otherwise.
        """
        ...

    def find_by_id(self, id_user: int) -> User:
        """
        Find a user by their identifier.

        Parameters
        ----------
        id_user : int
            Identifier of the user to find.

        Returns
        -------
        User or None
            User matching the given identifier, or None if not found.
        """
        ...

    def find_all(self) -> list[User]:
        """
        List all users in the database.

        Returns
        -------
        list of User
            All users, sorted by username.
        """
        ...

    def update(self, user) -> bool:
        """
        Update a user in the database.

        Password and access token are kept unchanged if they are None.

        Parameters
        ----------
        user : User
            User to update.

        Returns
        -------
        bool
            True if update is successful, False otherwise.
        """
        ...

    def delete(self, user) -> bool:
        """
        Delete a user from the database.

        Parameters
        ----------
        user : User
            User to delete.

        Returns
        -------
        bool
            True if the user was successfully deleted, False otherwise.
        """
        ...

    def login(self, username: str, password: str) -> User:
        """
        Find the user matching a username and a password.

        Parameters
        ----------
        username : str
            Username of the user.
        password : str
            Password of the user.

        Returns
        -------
        User or None
            The matching user, or None if the credentials are invalid.
        """
        ...

    def find_by_token(self, access_token: str) -> User:
        """
        Find a user by their access token.

        Parameters
        ----------
        access_token : str
            Token to search for.

        Returns
        -------
        User or None
            User matching the token, or None if not found or if the token
            is empty.
        """
        ...

    def find_by_username(self, username: str) -> User:
        """
        Find a user by their username.

        Parameters
        ----------
        username : str
            Username of the user to find.

        Returns
        -------
        User or None
            User matching the given username, or None if not found.
        """
        ...


# -----------------------------------------------------------------------------
# dao/project_dao.py
# -----------------------------------------------------------------------------
# [FIXED] "Arguments" is not a Numpy section -> "Parameters"
class ProjectDao(metaclass=Singleton):
    """
    Class containing methods to access Projects in the database.
    """

    def create(self, project: Project, id_user: int) -> bool:
        """
        Create a project in the database.

        The identifier generated by the database is set on ``project``.

        Parameters
        ----------
        project : Project
            Project to create.
        id_user : int
            Identifier of the user who owns the project.

        Returns
        -------
        bool
            True if creation is successful, False otherwise.
        """
        ...

    def find_by_id(self, id_project: int) -> Project | None:
        """
        Find a project by its identifier.

        Parameters
        ----------
        id_project : int
            Identifier of the project to find.

        Returns
        -------
        Project or None
            Project matching the given identifier, or None if not found.
        """
        ...

    def find_by_id_and_user(self, id_project: int, id_user: int) -> Project | None:
        """
        Find a project by its identifier, only if it belongs to the given user.

        Parameters
        ----------
        id_project : int
            Identifier of the project to find.
        id_user : int
            Identifier of the user who must own the project.

        Returns
        -------
        Project or None
            Project matching the given identifier and owned by the given
            user, or None if not found.
        """
        ...

    def list_all_project(self, id_user: int) -> list[Project]:
        """
        List all projects belonging to a given user.

        Parameters
        ----------
        id_user : int
            Identifier of the user whose projects are to be listed.

        Returns
        -------
        list of Project
            Projects of the user, or an empty list if there are none.
        """
        ...

    def update(self, project: Project) -> bool:
        """
        Update a project in the database.

        The secret HMAC key is kept unchanged if it is None.

        Parameters
        ----------
        project : Project
            Project to update.

        Returns
        -------
        bool
            True if update is successful, False otherwise.
        """
        ...

    def delete(self, project: Project) -> bool:
        """
        Delete a project from the database.

        Parameters
        ----------
        project : Project
            Project to delete.

        Returns
        -------
        bool
            True if the project was deleted, False otherwise.
        """
        ...

    def update_secret_key(self, project: Project) -> bool:
        """
        Replace the secret HMAC key of a project.

        Parameters
        ----------
        project : Project
            Project holding the new secret key.

        Returns
        -------
        bool
            True if the key was updated, False otherwise.
        """
        ...


# -----------------------------------------------------------------------------
# dao/audit_dao.py
# -----------------------------------------------------------------------------
class AuditDao(metaclass=Singleton):
    """
    Class containing methods to access Audits in the database.
    """

    @staticmethod
    def _row_to_audit(row: dict) -> Audit:
        """
        Convert a database row into an Audit object.

        Rebuilds the certificate (if signed) and the SBOM (an empty one
        if missing) stored with the audit.

        Parameters
        ----------
        row : dict
            Row of ``audit_table`` returned by the database.

        Returns
        -------
        Audit
            Audit corresponding to the row. Vulnerabilities, licences and
            antipatterns are not stored, so they are empty lists.
        """
        ...

    def create(self, audit: Audit) -> bool:
        """
        Create an audit in the database.

        The identifier and the date generated by the database are set
        on ``audit``.

        Parameters
        ----------
        audit : Audit
            Audit to create.

        Returns
        -------
        bool
            True if creation is successful, False otherwise.
        """
        ...

    def find_by_id(self, id_audit: int) -> Audit:
        """
        Find an audit by its identifier.

        Parameters
        ----------
        id_audit : int
            Identifier of the audit to find.

        Returns
        -------
        Audit or None
            Audit matching the given identifier, or None if not found.
        """
        ...

    def find_all(self) -> list[Audit]:
        """
        List all audits in the database.

        Returns
        -------
        list of Audit
            All audits, ordered by identifier.
        """
        ...

    def update(self, audit: Audit) -> bool:
        """
        Update an existing audit, including its certificate.

        Parameters
        ----------
        audit : Audit
            Audit to update.

        Returns
        -------
        bool
            True if update is successful, False otherwise.
        """
        ...

    def delete(self, audit: Audit) -> bool:
        """
        Delete an audit from the database.

        Parameters
        ----------
        audit : Audit
            Audit to delete.

        Returns
        -------
        bool
            True if the audit was deleted, False otherwise.
        """
        ...

    def list_all_audit(self, project: Project) -> list[Audit]:
        """
        List all audits of a given project.

        Parameters
        ----------
        project : Project
            Project whose audits are to be listed.

        Returns
        -------
        list of Audit
            Audits of the project, or an empty list if there are none.
        """
        ...


# -----------------------------------------------------------------------------
# schema/antipattern_model.py
# -----------------------------------------------------------------------------
def _class_name(value: Any) -> str:
    """
    Discriminator returning the class name of the business object.

    Parameters
    ----------
    value : Any
        Business object to serialize.

    Returns
    -------
    str
        Name of the class of ``value``.
    """
    ...


# [NEW]
class AntiPatternBase(BaseModel):
    """
    Base Pydantic model of an antipattern.

    Attributes
    ----------
    id_antipattern : int or None
        Unique identifier of the antipattern.
    line : int
        Line number where the antipattern was detected.
    description : str
        Description of the antipattern.
    """


# [NEW]
class NestedLoopModel(AntiPatternBase):
    """
    Pydantic model of a nested loop antipattern.

    Attributes
    ----------
    type : {'NestedLoop'}
        Type of the antipattern.
    depth : int
        Nesting depth of the loop.
    """


# [NEW]
class RecursiveCallModel(AntiPatternBase):
    """
    Pydantic model of a recursive call antipattern.

    Attributes
    ----------
    type : {'RecursiveCall'}
        Type of the antipattern.
    function_name : str
        Name of the function that calls itself.
    """


# -----------------------------------------------------------------------------
# schema/audit_model.py
# -----------------------------------------------------------------------------
# [NEW]
class AuditReadModel(BaseModel):
    """
    Model returned when the user consults a past audit.

    Attributes
    ----------
    id_audit : int
        Unique identifier of the audit.
    id_project : int
        Unique identifier of the audited project.
    date : datetime
        Date of the audit.
    complexity : float
        Complexity of the code.
    energy_consumption_kwh : float
        Energy consumption of the code (kWh).
    carbon_emission_gco2e : float
        Carbon emission of the code (gCO2e).
    quality_gate : QualityGateModel
        Quality gate of the audit.
    """


# [NEW]
class AuditResponseModel(BaseModel):
    """
    Model returned when the user runs an audit on a project.

    Attributes
    ----------
    id_audit : int
        Unique identifier of the audit.
    id_project : int
        Unique identifier of the audited project.
    date : datetime
        Date of the audit.
    vulnerabilities : list of VulnerabilityModel
        Vulnerabilities found in the dependencies.
    licenses : list of LicenceModel or str
        Licences used by the dependencies.
    anti_patterns : list of AntiPatternModel
        Antipatterns found in the code.
    complexity : float
        Complexity of the code.
    energy_consumption_kwh : float
        Energy consumption of the code (kWh).
    carbon_emission_gco2e : float
        Carbon emission of the code (gCO2e).
    quality_gate : QualityGateModel
        Quality gate of the audit.
    certificate : CertificateModel or None
        Certificate issued if the quality gate is respected.
    """


# [NEW]
class AuditCreateModel(BaseModel):
    """
    Model used to create the audit of a project.

    Attributes
    ----------
    project : ProjectCompletedModel
        Project to audit, with its code and dependency files.
    qualitygate_type : {'eco', 'security', 'global'}
        Type of quality gate to apply.
    hmac_signature : str
        HMAC signature of the request, encoded in Base64.
    """


# -----------------------------------------------------------------------------
# schema/certificate_model.py
# -----------------------------------------------------------------------------
class SignedCertificateModel(BaseModel):
    """
    Signed certificate: what the QR code contains.

    Attributes
    ----------
    payload : dict
        Signed data of the certificate.
    kid : str
        Identifier of the key used to sign.
    alg : str
        Signing algorithm (``'Ed25519'``).
    signature : str
        Signature of the payload.
    """


# [FIXED] "A COMPLETER"
class CertificateModel(BaseModel):
    """
    Certificate returned with an audit.

    Attributes
    ----------
    name : str
        Name of the certificate.
    type_file : str
        Format of the certificate file.
    date : datetime
        Generation date of the certificate.
    signed_data : SignedCertificateModel or None
        Signed data of the certificate.
    """


# [FIXED] "A COMPLETER"
class CertificateVerifyResponseModel(BaseModel):
    """
    Result of the verification of a certificate.

    Attributes
    ----------
    valid : bool
        True if the signature of the certificate is valid.
    payload : dict or None
        Payload of the certificate if valid.
    reason : str or None
        Reason of the failure if not valid.
    """


# -----------------------------------------------------------------------------
# schema/codefile_model.py
# -----------------------------------------------------------------------------
# [NEW]
class CodeFileModel(BaseModel):
    """
    Code file sent by the client.

    Attributes
    ----------
    name : str
        Name of the file.
    content : str
        Content of the file, encoded in Base64.
    type_file : str
        Extension of the file.
    """


# -----------------------------------------------------------------------------
# schema/dependencyfile_model.py
# -----------------------------------------------------------------------------
# [NEW]
class DependencyFileModel(BaseModel):
    """
    Dependency file sent by the client.

    Attributes
    ----------
    name : str
        Name of the file.
    content : str
        Content of the file, encoded in Base64.
    type_file : str
        Extension of the file.
    """


# -----------------------------------------------------------------------------
# schema/licence_model.py
# -----------------------------------------------------------------------------
# [NEW]
class LicenceModel(BaseModel):
    """
    Pydantic model of a licence.

    Attributes
    ----------
    id_licence : int or None
        Unique identifier of the licence.
    name : str
        Name of the licence (SPDX identifier).
    risk_level : str
        Risk level associated with the licence.
    """


# -----------------------------------------------------------------------------
# schema/project_model.py
# -----------------------------------------------------------------------------
# [NEW]
class ProjectReadModel(BaseModel):
    """
    Model returned when the user consults a project.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    name_project : str
        Name of the project.
    """


# [NEW]
class ProjectResponseModel(BaseModel):
    """
    Model returned when a project is created.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    name_project : str
        Name of the project.
    secretHMACkey : str
        Secret HMAC key of the project, encoded in Base64.
    """


# [NEW]
class ProjectCreateModel(BaseModel):
    """
    Model used to create or rename a project.

    Attributes
    ----------
    name_project : str
        Name of the project.
    """


# [NEW]
class ProjectCompletedModel(BaseModel):
    """
    Project sent with its files to be audited.

    Attributes
    ----------
    id_project : int
        Unique identifier of the project.
    codefile : CodeFileModel
        Code file of the project.
    dependencyfile : DependencyFileModel
        Dependency file of the project.
    """


# -----------------------------------------------------------------------------
# schema/qualitygate_model.py
# -----------------------------------------------------------------------------
# [NEW]
class QualityGateModel(BaseModel):
    """
    Pydantic model of a quality gate.

    Attributes
    ----------
    status : str
        Status of the quality gate.
    """


# -----------------------------------------------------------------------------
# schema/user_model.py
# -----------------------------------------------------------------------------
class UserModel(BaseModel):
    """
    Data contract between the frontend and the backend for a user.

    Defines the JSON structure used to exchange user information,
    ensuring data consistency and validation during API requests and
    responses.

    Attributes
    ----------
    username : str
        Name of the user.
    password : str
        Password of the user (at least 16 characters).
    email : EmailStr
        Email of the user.
    """

    # [NEW]
    @classmethod
    def check_password_length(cls, v: str) -> str:
        """
        Check that the password is long enough.

        Parameters
        ----------
        v : str
            Password to validate.

        Returns
        -------
        str
            The password, unchanged.

        Raises
        ------
        ValueError
            If the password has fewer than 16 characters.
        """
        ...


# [FIXED] "DOC A FAIRE"
class UserResponseModel(BaseModel):
    """
    Model used to update an existing user.

    Attributes
    ----------
    id_user : int
        Unique identifier of the user.
    username : str
        Name of the user.
    password : str
        Password of the user.
    email : EmailStr
        Email of the user.
    """


# [NEW]
class UserReadModel(BaseModel):
    """
    Model returned when user information is read.

    Attributes
    ----------
    id_user : int
        Unique identifier of the user.
    username : str
        Name of the user.
    email : EmailStr
        Email of the user.
    access_token : str or None
        Access token of the user.
    """


# [NEW]
class UserLoginModel(BaseModel):
    """
    Credentials sent to log in.

    Attributes
    ----------
    username : str
        Name of the user.
    password : str
        Password of the user.
    """


# -----------------------------------------------------------------------------
# schema/vulnerability_model.py
# -----------------------------------------------------------------------------
def _class_name(value: Any) -> str:
    """
    Discriminator returning the class name of the business object.

    Parameters
    ----------
    value : Any
        Business object to serialize.

    Returns
    -------
    str
        Name of the class of ``value``.
    """
    ...


# [NEW]
class VulnerabilityBase(BaseModel):
    """
    Base Pydantic model of a vulnerability.

    Attributes
    ----------
    id_vulnerability : int or None
        Unique identifier of the vulnerability.
    osv_id : str
        Identifier given by the OSV API.
    cve_id : str or None
        CVE identifier of the vulnerability.
    package : str
        Package affected by the vulnerability.
    version_package : str
        Version of the affected package.
    """


# [NEW]
class LowVulnerabilityModel(VulnerabilityBase):
    """
    Pydantic model of a low severity vulnerability.

    Attributes
    ----------
    severity : {'low'}
        Severity of the vulnerability.
    """


# [NEW]
class MediumVulnerabilityModel(VulnerabilityBase):
    """
    Pydantic model of a medium severity vulnerability.

    Attributes
    ----------
    severity : {'medium'}
        Severity of the vulnerability.
    """


# [NEW]
class HighVulnerabilityModel(VulnerabilityBase):
    """
    Pydantic model of a high severity vulnerability.

    Attributes
    ----------
    severity : {'high'}
        Severity of the vulnerability.
    """


# [NEW]
class CriticalVulnerabilityModel(VulnerabilityBase):
    """
    Pydantic model of a critical severity vulnerability.

    Attributes
    ----------
    severity : {'critical'}
        Severity of the vulnerability.
    """


# =============================================================================
#  PARTIE 3 — service/
# =============================================================================


# -----------------------------------------------------------------------------
# service/audit_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class AuditService:
    """
    Service that handles business logic related to the audit of a project.

    Methods
    -------
    create(...)
        Create a new audit and store it.
    find_by_id(id_audit)
        Find an audit by its identifier.
    list_all_audit(id_project)
        List all the audits.
    update(audit)
        Update an audit.
    run_audit(project, quality_gate_type)
        Run a full audit on a project.
    """

    def create(self, id_project, date, vulnerabilities, licenses, anti_patterns, complexity,
               energy_consumption_kwh, carbon_emission_gco2e, sbom, quality_gate,
               certificate) -> Audit:
        """
        Create a new audit in the system.

        Parameters
        ----------
        id_project : int
            Unique identifier of the project linked to this audit.
        date : datetime
            Date the audit was created.
        vulnerabilities : list of Vulnerability
            Vulnerabilities found in the dependencies of the project.
        licenses : list of Licence
            Licences used by the dependencies of the project.
        anti_patterns : list of AntiPattern
            Antipatterns found in the project.
        complexity : float
            Complexity of the code.
        energy_consumption_kwh : float
            Energy consumption of the code (kWh).
        carbon_emission_gco2e : float
            Carbon emission of the code (gCO2e).
        sbom : SBOMFile
            Software Bill of Materials, the inventory of components used
            by the project.
        quality_gate : QualityGate
            Quality gate associated with the project.
        certificate : CertificateFile or None
            Certificate associated with the audit.

        Returns
        -------
        Audit or None
            The created audit, or None if the creation failed.
        """
        ...

    def find_by_id(self, id_audit: int) -> Audit:
        """
        Find an audit by its identifier.

        Parameters
        ----------
        id_audit : int
            Identifier of the audit.

        Returns
        -------
        Audit or None
            The audit found, or None if the search failed.
        """
        ...

    def list_all_audit(self, id_project: int) -> list[Audit]:
        """
        List all the audits of a project.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        list of Audit
            Audits of the project.
        """
        ...

    def update(self, audit: Audit):
        """
        Update an audit.

        Parameters
        ----------
        audit : Audit
            Audit to update.

        Returns
        -------
        bool
            True if the update is successful, False otherwise.
        """
        ...

    def run_audit(self, project: Project, quality_gate_type: str):
        """
        Run a full audit on a project.

        Finds the vulnerabilities and licences of the dependencies, analyses
        the code (antipatterns, complexity, energy, carbon), generates the
        SBOM, evaluates the quality gate and, if it is passed, generates
        a certificate.

        Parameters
        ----------
        project : Project
            Project to audit, with its code file and dependency file.
        quality_gate_type : str
            Type of quality gate to apply (``'eco'``, ``'security'`` or
            ``'global'``).

        Returns
        -------
        Audit
            The completed audit.
        """
        ...


# -----------------------------------------------------------------------------
# service/certificate_service.py
# -----------------------------------------------------------------------------
# [NEW]
class CertificateService:
    """
    Service that generates, signs and verifies audit certificates.

    Methods
    -------
    generate_certificate(audit, project, qualitygate_type)
        Generate a signed PDF certificate for an audited project.
    sign_certificate(payload)
        Sign a certificate payload with the application's private key.
    verify_certificate(certificate)
        Check a signed certificate against the application's public key.
    """

    def generate_certificate(self, audit: Audit, project: Project,
                             qualitygate_type: str) -> CertificateFile:
        """
        Generate a signed PDF certificate for an audited project.

        The PDF embeds a QR code containing the signed certificate
        (payload, kid, signature), so it can be verified without database
        access.

        Parameters
        ----------
        audit : Audit
            Audit whose quality gate was passed.
        project : Project
            Audited project.
        qualitygate_type : str
            Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).

        Returns
        -------
        CertificateFile
            Certificate containing the PDF in bytes and the signed data.

        Raises
        ------
        ValueError
            If the quality gate type is unknown.
        """
        ...

    @staticmethod
    def sign_certificate(payload: dict) -> dict:
        """
        Sign a certificate payload with the application's private key.

        Parameters
        ----------
        payload : dict
            Data of the certificate to sign.

        Returns
        -------
        dict
            Signed certificate containing ``payload``, ``kid``, ``alg``
            and ``signature`` (encoded in Base64).
        """
        ...

    @staticmethod
    def verify_certificate(certificate: dict) -> bool:
        """
        Check a signed certificate against the application's public key.

        Parameters
        ----------
        certificate : dict
            Signed certificate (``payload``, ``kid``, ``alg``, ``signature``).

        Returns
        -------
        bool
            True if the key identifier matches and the signature is valid,
            False otherwise.
        """
        ...


# -----------------------------------------------------------------------------
# service/eco_service.py
# -----------------------------------------------------------------------------
class AstAnalysis:
    """
    Result of ONE analysis of the code (parsed once).

    Attributes
    ----------
    metrics : dict
        Metrics extracted from the AST.
    antipatterns : list of AntiPattern
        Antipatterns detected in the code.
    complexity : float
        Estimated complexity of the code.
    energy_kwh : float
        Estimated energy consumption (kWh).
    carbon_gco2e : float
        Estimated carbon emission (gCO2e).
    """


class EcoService:
    """
    Service responsible for AST analysis, energy estimation and carbon
    estimation.

    Attributes
    ----------
    OPERATIONS_PER_SECOND : int
        Number of operations executed per second by the reference CPU.
    CPU_POWER_W : float
        Power of the reference CPU (W).
    CARBON_INTENSITY_GCO2E_PER_KWH : float
        Default carbon intensity of electricity (gCO2e/kWh).
    DEFAULT_LOOP_LENGTH : int
        Number of iterations assumed when the length of a loop is unknown.
    DEFAULT_RECURSION_DEPTH : int
        Recursion depth assumed for recursive functions.
    """

    @staticmethod
    def parse(code_file: CodeFile) -> ast.Module:
        """
        Parse Python source code and return its AST.

        Parameters
        ----------
        code_file : CodeFile
            Code file to parse. Its content may be ``str`` or ``bytes``
            (decoded as UTF-8).

        Returns
        -------
        ast.Module
            Abstract Syntax Tree of the code.

        Raises
        ------
        TypeError
            If the content of the file is neither ``str`` nor ``bytes``.
        SyntaxError
            If the code is not valid Python.
        """
        ...

    def analyze(self, code_file: CodeFile, input_size: int = 1000) -> AstAnalysis:
        """
        Run the full eco analysis of a code file.

        The code is parsed only once, then used to compute the antipatterns,
        the metrics, the complexity, the energy and the carbon emission.

        Parameters
        ----------
        code_file : CodeFile
            Code file to analyse.
        input_size : int, default 1000
            Assumed size of the input data, used to estimate the energy.

        Returns
        -------
        AstAnalysis
            Result of the analysis.
        """
        ...

    def _extract_metrics(self, tree: ast.Module, antipatterns: list[AntiPattern]) -> dict:
        """
        Extract simple counts from the AST with a single ``ast.walk``.

        Loop depth and recursive functions are reused from the antipatterns
        (not recomputed).

        Parameters
        ----------
        tree : ast.Module
            AST of the code.
        antipatterns : list of AntiPattern
            Antipatterns already detected in the code.

        Returns
        -------
        dict
            Metrics: ``ast_nodes``, ``loops``, ``nested_loops_depth``,
            ``conditions``, ``function_calls``, ``operations`` and
            ``recursive_functions``.
        """
        ...

    # [NEW]
    def calculate_energy(self, metrics: dict, input_size: int = 1000) -> float:
        """
        Estimate the energy consumption of the code.

        The number of operations is multiplied by ``input_size`` raised to
        the loop nesting depth, and once more if there is recursion.

        Parameters
        ----------
        metrics : dict
            Metrics returned by ``_extract_metrics``.
        input_size : int, default 1000
            Assumed size of the input data.

        Returns
        -------
        float
            Estimated energy consumption (kWh).

        Raises
        ------
        ValueError
            If ``input_size`` is lower than 1.
        """
        ...

    def calculate_carbon(self, energy_kwh: float,
                         carbon_intensity_gco2e_per_kwh: float | None = None) -> float:
        """
        Calculate carbon emissions in gCO2e.

        Parameters
        ----------
        energy_kwh : float
            Energy consumption (kWh).
        carbon_intensity_gco2e_per_kwh : float or None, optional
            Carbon intensity of electricity (gCO2e/kWh). Uses
            ``CARBON_INTENSITY_GCO2E_PER_KWH`` if None.

        Returns
        -------
        float
            Carbon emission (gCO2e).

        Raises
        ------
        ValueError
            If the energy or the carbon intensity is negative.
        """
        ...

    @staticmethod
    def _outest_loop(tree: ast.AST) -> list[ast.stmt]:
        """
        Find all the loops that are not nested in another loop.

        Parameters
        ----------
        tree : ast.AST
            AST of the code (or of a node).

        Returns
        -------
        list of ast.stmt
            Outermost ``for`` and ``while`` loops.
        """
        ...

    @staticmethod
    def _loop_depth(node: ast.AST) -> int:
        """
        Compute the loop nesting depth of a node.

        Parameters
        ----------
        node : ast.AST
            Node to analyse.

        Returns
        -------
        int
            Maximum number of nested loops under the node (the node
            included).
        """
        ...

    @staticmethod
    def _is_recursive_call(call: ast.Call, function_name: str) -> bool:
        """
        Check whether a call is a recursive call.

        Parameters
        ----------
        call : ast.Call
            Call inside a function named ``function_name``.
        function_name : str
            Name of the function.

        Returns
        -------
        bool
            True if the call refers to the function named ``function_name``.
        """
        ...

    def detect_antipatterns(self, tree: ast.Module) -> list[AntiPattern]:
        """
        Detect all the antipatterns in a Python code.

        Parameters
        ----------
        tree : ast.Module
            AST (Abstract Syntax Tree) of the code.

        Returns
        -------
        list of AntiPattern
            Nested loops (depth >= 2) and recursive calls found in the code.
        """
        ...

    @staticmethod
    def _loop_length(node: ast.stmt) -> int:
        """
        Calculate the number of iterations of a loop.

        Parameters
        ----------
        node : ast.stmt
            ``for`` or ``while`` loop.

        Returns
        -------
        int
            Number of iterations of the loop, or ``DEFAULT_LOOP_LENGTH``
            if it cannot be known statically.
        """
        ...

    @staticmethod
    def _loop_complexity(node: ast.stmt) -> int:
        """
        Calculate the complexity of a loop, including its inner loops.

        Parameters
        ----------
        node : ast.stmt
            Loop to analyse.

        Returns
        -------
        int
            Complexity of the loop.
        """
        ...

    @staticmethod
    def _count_recursive_calls(node: ast.AST, function_name: str) -> int:
        """
        Count the recursive calls made by one execution of a function.

        A call inside a loop is counted once per iteration.

        Parameters
        ----------
        node : ast.AST
            Function to analyse.
        function_name : str
            Name of the function.

        Returns
        -------
        int
            Number of recursive calls.
        """
        ...

    def estimate_complexity(self, tree: ast.Module) -> float:
        """
        Estimate the complexity of a Python code.

        Parameters
        ----------
        tree : ast.Module
            AST of the code to estimate.

        Returns
        -------
        float
            Complexity of the code.
        """
        ...


# -----------------------------------------------------------------------------
# service/project_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class ProjectService:
    """
    Service that handles business logic related to a project (upload, update, etc.).
    """

    def upload(self, project_name: str, user: User) -> Project | None:
        """
        Create a new project in the system.

        A new secret HMAC key is generated for the project.

        Parameters
        ----------
        project_name : str
            Name of the project.
        user : User
            User that owns the project.

        Returns
        -------
        Project or None
            The created project, or None if the creation failed.
        """
        ...

    def find_by_id(self, id_project: int) -> Project | None:
        """
        Find a project by its unique identifier.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        Project or None
            The project if found, otherwise None.
        """
        ...

    def find_by_id_and_user(self, id_project: int, id_user: int) -> Project | None:
        """
        Find a project by its identifier, only if it belongs to the given user.

        Parameters
        ----------
        id_project : int
            Identifier of the project.
        id_user : int
            Identifier of the user.

        Returns
        -------
        Project or None
            The project if found and owned by the user, otherwise None.
        """
        ...

    def update(self, project: Project) -> Project | None:
        """
        Update an existing project's information.

        Parameters
        ----------
        project : Project
            Project containing the updated information.

        Returns
        -------
        Project or None
            The updated project, or None if the update failed.
        """
        ...

    def delete(self, project: Project) -> bool:
        """
        Delete a project.

        Parameters
        ----------
        project : Project
            Project to delete.

        Returns
        -------
        bool
            True if the deletion was successful, False otherwise.
        """
        ...

    @staticmethod
    def verify_signature(project: Project, signature: bytes) -> bool:
        """
        Verify the HMAC signature sent with a project.

        Parameters
        ----------
        project : Project
            Project related to the signature, with its files.
        signature : bytes
            Signature to verify.

        Returns
        -------
        bool
            True if the signature is valid, False otherwise.
        """
        ...

    def list_all_audit(self, id_project: int) -> list[Audit] | None:
        """
        List all the audits of a project.

        Parameters
        ----------
        id_project : int
            Identifier of the project.

        Returns
        -------
        list of Audit or None
            Audits of the project, or None if the project does not exist.
        """
        ...

    def regenerate_secret_key(self, project: Project) -> str | None:
        """
        Generate and store a new secret key for the project.

        Parameters
        ----------
        project : Project
            Project whose secret key is regenerated.

        Returns
        -------
        str or None
            The new key encoded in Base64, or None if the update failed.
        """
        ...


# -----------------------------------------------------------------------------
# service/qualitygate_service.py
# -----------------------------------------------------------------------------
# [CONVERTED] + remove the duplicated class docstring
class QualityGateService:
    """
    Service that handles business logic related to a quality gate.
    """

    def create(self, type_qualitygate, max_vulnerabilities, max_critical_vulnerabilities,
               max_carbon_emission, max_energy_consumption, status) -> QualityGate:
        """
        Create a QualityGate object of the chosen type.

        Parameters
        ----------
        type_qualitygate : str
            Type of the quality gate (``'eco'``, ``'security'`` or ``'global'``).
        max_vulnerabilities : int
            Maximum number of vulnerabilities tolerated for a project.
        max_critical_vulnerabilities : int
            Maximum number of critical vulnerabilities tolerated for a project.
        max_carbon_emission : float
            Maximum carbon emission tolerated for a project.
        max_energy_consumption : float
            Maximum energy consumption tolerated for a project.
        status : str
            Status of the quality gate.

        Returns
        -------
        QualityGate
            Quality gate of the requested type.

        Raises
        ------
        ValueError
            If the requested type is not supported.
        """
        ...

    def evaluate(self, qualitygate: QualityGate, audit: Audit):
        """
        Evaluate the audit of a project with the chosen quality gate.

        The quality gate is attached to the audit and its status is set
        to ``'Passed'`` or ``'Failed'``.

        Parameters
        ----------
        qualitygate : QualityGate
            Quality gate chosen for the evaluation.
        audit : Audit
            Audit of the project to evaluate.

        Returns
        -------
        None
        """
        ...


# -----------------------------------------------------------------------------
# service/sbom_service.py
# -----------------------------------------------------------------------------
class SBOMService:
    """
    Generate the SBOM (CycloneDX, JSON) of a project.
    """

    @staticmethod
    def _normalize(name: str, ecosystem: str) -> str:
        """
        Normalize the name of a package.

        Applies PEP 503 normalization for PyPI, lowercase for the others.

        Parameters
        ----------
        name : str
            Name of the package.
        ecosystem : str
            Purl type of the ecosystem (e.g. ``'pypi'``).

        Returns
        -------
        str
            Normalized name of the package.
        """
        ...

    def generate(self, project, vulnerabilities) -> SBOMFile:
        """
        Generate the SBOM (CycloneDX, JSON) of a project.

        Parameters
        ----------
        project : Project
            Project to inventory.
        vulnerabilities : list of Vulnerability, optional
            Vulnerabilities found by SecurityService (instances of
            ``CriticalVulnerability``, ``HighVulnerability``,
            ``MediumVulnerability`` or ``LowVulnerability``). They are
            added to the SBOM and linked to the affected component. The
            severity is deduced from the class of each vulnerability.

        Returns
        -------
        SBOMFile
            SBOM whose content is the JSON document in bytes.

        Raises
        ------
        ValueError
            If the project is None.
        """
        ...

    # [NEW]
    def create_empty_sbom(self):
        """
        Create an empty SBOM.

        Used when an audit has no stored SBOM.

        Returns
        -------
        SBOMFile
            SBOM named ``'Empty'`` whose content is ``b'0'``.
        """
        ...


# -----------------------------------------------------------------------------
# service/security_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class SecurityService:
    """
    Service that finds the vulnerabilities and the licences of the
    dependencies of a project.
    """

    def detect_ecosystem(self, dependencyfile: DependencyFile) -> str:
        """
        Find the ecosystem related to the dependency file.

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        str
            Name of the ecosystem (``'PyPI'``, ``'npm'``, ``'Maven'`` or
            ``'crates.io'``).

        Raises
        ------
        ValueError
            If the file is not supported.
        """
        ...

    def find_vulnerabilities(self, dep_file: DependencyFile) -> list[Vulnerability]:
        """
        Find the vulnerabilities of the dependencies using the OSV API.

        Parameters
        ----------
        dep_file : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Vulnerability
            Vulnerabilities found for the dependencies of the file.
        """
        ...

    def find_licences(self, dep_file: DependencyFile) -> list[Licence]:
        """
        Find all the licences of the dependencies using the deps.dev API.

        Parameters
        ----------
        dep_file : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Licence
            Licences found in the file, without duplicates.
        """
        ...


# -----------------------------------------------------------------------------
# service/user_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class UserService:
    """
    Service that handles business logic related to a user.
    """

    def create(self, username: str, password: str, email: str) -> User:
        """
        Create a new user in the system.

        Parameters
        ----------
        username : str
            Name of the user.
        password : str
            Password of the user.
        email : str
            Email of the user.

        Returns
        -------
        User or None
            The created user, or None if the creation failed.
        """
        ...

    def find_by_id(self, id: int) -> User:
        """
        Find a user by their identifier.

        Parameters
        ----------
        id : int
            Identifier of the user to find.

        Returns
        -------
        User or None
            The user found, or None if the search failed.
        """
        ...

    def update(self, user: User) -> User:
        """
        Update a user.

        Parameters
        ----------
        user : User
            User to update.

        Returns
        -------
        User or None
            The updated user, or None if the update failed.
        """
        ...

    def delete(self, user: User) -> bool:
        """
        Delete a user.

        Parameters
        ----------
        user : User
            User to delete.

        Returns
        -------
        bool
            True if the deletion is successful, False otherwise.
        """
        ...

    def login(self, username: str, password: str) -> User:
        """
        Log a user in with their username and password.

        A new access token is generated and stored for the user.

        Parameters
        ----------
        username : str
            Username of the user.
        password : str
            Password of the user.

        Returns
        -------
        User or None
            The logged in user with their access token, or None if the
            credentials are invalid.
        """
        ...

    def username_already_used(self, username: str) -> bool:
        """
        Check whether a username is already used.

        Parameters
        ----------
        username : str
            Username to check.

        Returns
        -------
        bool
            True if the username is already used, False otherwise.
        """
        ...

    def list_all_project(self, id_user: int) -> list[Project] | None:
        """
        List all the projects owned by a user.

        Parameters
        ----------
        id_user : int
            Identifier of the user.

        Returns
        -------
        list of Project or None
            Projects owned by the user, or None if the user does not exist.
        """
        ...


# -----------------------------------------------------------------------------
# service/vulnerability_service.py
# -----------------------------------------------------------------------------
class VulnerabilityService:
    """
    Service containing business logic for vulnerabilities.
    """

    @staticmethod
    def get_critical_vulnerability_count(vulnerabilities: list) -> int:
        """
        Return the number of critical vulnerabilities.

        Parameters
        ----------
        vulnerabilities : list of Vulnerability or None
            Vulnerabilities to count.

        Returns
        -------
        int
            Number of ``CriticalVulnerability`` instances in the list.
        """
        ...


# =============================================================================
#  PARTIE 4 — service/file_services/, utils/
# =============================================================================


# -----------------------------------------------------------------------------
# service/file_services/file_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class FileService:
    """
    Service that handles business logic related to a file.
    """

    def get_filename(self, dependencyfile: DependencyFile) -> str:
        """
        Get the full filename of the dependency file.

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing the dependencies.

        Returns
        -------
        str
            Name of the file with its extension (e.g. ``'requirements.txt'``).
        """
        ...

    def parse_dependencies(self, dependencyfile: DependencyFile) -> list[Dependency]:
        """
        Find all the dependencies in the dependency file.

        The parser is chosen according to the extension of the file
        (``txt``, ``json``, ``xml`` or ``toml``).

        Parameters
        ----------
        dependencyfile : DependencyFile
            File containing all the dependencies.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.

        Raises
        ------
        ValueError
            If the extension of the file is not supported.
        """
        ...


# -----------------------------------------------------------------------------
# service/file_services/txt_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class TxtService:
    """
    Service that parses ``.txt`` dependency files (``requirements.txt``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.txt`` file.

        Comments, empty lines and pip options (``-r``, ``-e``...) are
        ignored. Only exact versions (``==``) are kept.

        Parameters
        ----------
        content : bytes
            Content of the ``.txt`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        ...


# -----------------------------------------------------------------------------
# service/file_services/json_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class JsonService:
    """
    Service that parses ``.json`` dependency files (``package.json``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.json`` file.

        Reads both ``dependencies`` and ``devDependencies``.

        Parameters
        ----------
        content : bytes
            Content of the ``.json`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        ...


# -----------------------------------------------------------------------------
# service/file_services/xml_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class XmlService:
    """
    Service that parses ``.xml`` dependency files (``pom.xml``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.xml`` file.

        Each dependency is named ``'groupId:artifactId'``.

        Parameters
        ----------
        content : bytes
            Content of the ``.xml`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        ...


# -----------------------------------------------------------------------------
# service/file_services/toml_service.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class TomlService:
    """
    Service that parses ``.toml`` dependency files (``Cargo.toml``).
    """

    def parse_dependencies(self, content: bytes) -> list[Dependency]:
        """
        Find all the dependencies in the content of a ``.toml`` file.

        Reads the ``[dependencies]`` table.

        Parameters
        ----------
        content : bytes
            Content of the ``.toml`` file.

        Returns
        -------
        list of Dependency
            Dependencies found in the file.
        """
        ...


# -----------------------------------------------------------------------------
# service/file_services/py_service.py
# -----------------------------------------------------------------------------
class PyService:
    """
    Service that handles ``.py`` files.
    """


# -----------------------------------------------------------------------------
# service/file_services/js_service.py
# -----------------------------------------------------------------------------
class JsService:
    """
    Service that handles ``.js`` files.
    """


# -----------------------------------------------------------------------------
# service/file_services/java_service.py
# -----------------------------------------------------------------------------
class JavaService:
    """
    Service that handles ``.java`` files.
    """


# -----------------------------------------------------------------------------
# utils/env_variables.py
# -----------------------------------------------------------------------------
# [CONVERTED]
def load_environment_variables():
    """
    Load environment variables from the ``.env`` file.

    Existing variables are overridden.

    Returns
    -------
    None
    """
    ...


def mask_value(key, value):
    """
    Mask sensitive values based on their key name.

    Parameters
    ----------
    key : str
        Name of the environment variable.
    value : str
        Actual value of the environment variable.

    Returns
    -------
    str
        ``'*******'`` if the key contains a sensitive keyword (PASSWORD,
        SECRET, KEY, TOKEN), otherwise the original value.
    """
    ...


def display_values(include_prefix=None, exclude_prefix=None):
    """
    Log all environment variables, masking sensitive values.

    Parameters
    ----------
    include_prefix : str, optional
        If provided, only keys starting with this prefix are logged.
    exclude_prefix : str, optional
        If provided, keys starting with this prefix are skipped.

    Returns
    -------
    None
    """
    ...


# -----------------------------------------------------------------------------
# utils/generate_signing_key.py
# -----------------------------------------------------------------------------
# [NEW] module docstring (the script has no function)
"""
Generate a new Ed25519 signing key pair.

Prints the private key in PEM format, on one line, ready to be copied
into the ``CERT_SIGNING_PRIVATE_KEY`` environment variable.
"""


# -----------------------------------------------------------------------------
# utils/log_utils.py
# -----------------------------------------------------------------------------
def initialize_logs(name: str):
    """
    Initialize logging from the ``logging_config.yml`` configuration file.

    Creates the ``logs`` folder at the root of the project if it does
    not exist.

    Parameters
    ----------
    name : str
        Name of the application, written in the first log lines.

    Returns
    -------
    None
    """
    ...


def get_logger(module_name: str, max_size: int = 25):
    """
    Return a logger with a shortened name based on the module path.

    If the path exceeds ``max_size``, the initials of the prefix parts
    are used (e.g. ``'s.f.file_service'``).

    Parameters
    ----------
    module_name : str
        Full name of the module (usually ``__name__``).
    max_size : int, default 25
        Maximum length of the name before it is shortened.

    Returns
    -------
    logging.Logger
        Logger with the (possibly shortened) name.
    """
    ...


class LogIndentation:
    """
    Indent logs when entering a new method.

    Attributes
    ----------
    current_indentation : int
        Current indentation level.
    indentation_size : int
        Number of spaces per indentation level.
    """

    @classmethod
    def increase_indentation(cls):
        """
        Increase the indentation level by one.

        Returns
        -------
        None
        """
        ...

    @classmethod
    def decrease_indentation(cls):
        """
        Decrease the indentation level by one.

        Returns
        -------
        None
        """
        ...

    @classmethod
    def get_indentation(cls):
        """
        Get the current indentation.

        Returns
        -------
        str
            Spaces corresponding to the current indentation level.
        """
        ...


def log(func):
    """
    Decorator to log method calls and their outputs.

    When applied to a method, it logs the call with the parameter values
    (sensitive values such as passwords or keys are masked) and the
    return value of the method (shortened if too long).

    Parameters
    ----------
    func : callable
        Method to decorate.

    Returns
    -------
    callable
        Wrapped method.
    """
    ...


class LogMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs every HTTP request and response.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Log an HTTP request and its response.

        Captures the method, the path, the status code and the error
        details.

        Parameters
        ----------
        request : Request
            Incoming HTTP request.
        call_next : callable
            Function that passes the request to the next handler.

        Returns
        -------
        Response
            Response returned by the next handler.

        Raises
        ------
        Exception
            Any exception raised while handling the request, re-raised
            after being logged.
        """
        ...


# -----------------------------------------------------------------------------
# utils/reset_database.py
# -----------------------------------------------------------------------------
class ResetDatabase(metaclass=Singleton):
    """
    Database reset utility.

    Attributes
    ----------
    base_path : pathlib.Path
        Root folder of the project, containing the ``data`` folder.
    """

    def run(self, test_dao=False):
        """
        Run the database reset.

        Drops and recreates the schema, runs ``init_db.sql`` and
        ``pop_db.sql``, then hashes the passwords of all users.

        Parameters
        ----------
        test_dao : bool, default False
            If True, reset the test data (currently not used).

        Returns
        -------
        bool
            True if the reset succeeded.

        Raises
        ------
        FileNotFoundError
            If an SQL file cannot be found.
        Exception
            If an SQL query fails.
        """
        ...


# -----------------------------------------------------------------------------
# utils/security.py
# -----------------------------------------------------------------------------
# [CONVERTED]
def hash_password(password: str, salt: str = "") -> str:
    """
    Hash a password using the SHA-256 algorithm.

    Parameters
    ----------
    password : str
        Plain text password to hash.
    salt : str, optional
        String added to the password before hashing to protect against
        rainbow table attacks.

    Returns
    -------
    str
        Resulting hexadecimal hash string.
    """
    ...


def verify_token(x_auth_token=Header(None)) -> User:
    """
    Verify the authenticity of a user via the provided auth token.

    Checks that a token is present in the request headers and validates
    it against the database.

    Parameters
    ----------
    x_auth_token : str, optional
        Token extracted from the ``X-Auth-Token`` HTTP header.

    Returns
    -------
    User
        User associated with the valid token.

    Raises
    ------
    HTTPException
        401 error if the token is missing or not found in the database.
    """
    ...


def generate_secret_HMAC_key() -> bytes:
    """
    Generate a new secret HMAC key.

    Returns
    -------
    bytes
        New random secret key of 32 bytes.
    """
    ...


def encode_secret_key(key: bytes | str) -> str:
    """
    Encode a binary secret key as a Base64 string.

    Parameters
    ----------
    key : bytes or str
        Key to convert. A ``str`` is returned unchanged.

    Returns
    -------
    str
        Base64 representation of the key.
    """
    ...


def generate_signature(secret: bytes, project_id_bytes: bytes, code: bytes,
                       dependency: bytes) -> bytes:
    """
    Generate the HMAC-SHA256 signature of a project submission.

    Each element is prefixed with its length, so that the boundaries
    between the elements cannot be shifted.

    Parameters
    ----------
    secret : bytes
        Secret HMAC key of the project.
    project_id_bytes : bytes
        Identifier of the project, encoded in UTF-8.
    code : bytes
        Content of the code file.
    dependency : bytes
        Content of the dependency file.

    Returns
    -------
    bytes
        Signature associated with the secret and the files.
    """
    ...


def load_signing_key() -> Ed25519PrivateKey:
    """
    Load the application's private signing key from the environment.

    The key is read from ``CERT_SIGNING_PRIVATE_KEY`` and cached.

    Returns
    -------
    Ed25519PrivateKey
        Private signing key of the application.

    Raises
    ------
    RuntimeError
        If ``CERT_SIGNING_PRIVATE_KEY`` is missing.
    """
    ...


def get_public_key_pem() -> str:
    """
    Return the public key in PEM format, safe to expose.

    Returns
    -------
    str
        Public key in PEM format.
    """
    ...


def get_key_id() -> str:
    """
    Return the fingerprint of the public key, used as ``kid`` in certificates.

    Returns
    -------
    str
        First 16 hexadecimal characters of the SHA-256 of the public key.
    """
    ...


def canonical_json(payload: dict) -> bytes:
    """
    Serialize a payload deterministically, as required for stable signatures.

    Parameters
    ----------
    payload : dict
        Data to serialize.

    Returns
    -------
    bytes
        JSON with sorted keys and no spaces, encoded in UTF-8.
    """
    ...


# -----------------------------------------------------------------------------
# utils/singleton.py
# -----------------------------------------------------------------------------
class Singleton(type):
    """
    Metaclass ensuring that a class has only one instance.

    All classes that use Singleton as metaclass will have only one
    instance (https://refactoring.guru/fr/design-patterns/singleton).
    """

    # [NEW]
    def __call__(cls, *args, **kwargs):
        """
        Return the unique instance of the class, creating it if needed.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to the constructor.
        **kwargs : dict
            Keyword arguments passed to the constructor.

        Returns
        -------
        object
            Unique instance of the class.
        """
        ...


# =============================================================================
#  PARTIE 5 — frontend/ (Streamlit)
# =============================================================================
#  Les pages Streamlit sont des scripts sans fonction : on leur ajoute une
#  docstring de module (à coller tout en haut du fichier, avant les imports).


# -----------------------------------------------------------------------------
# frontend/app.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Entry point of the CleanOps Streamlit application.

Configures the page, initializes logs and environment variables once per
session, and builds the navigation menu: private pages (projects, new
audit, audits) are only shown to logged in users.
"""


# -----------------------------------------------------------------------------
# frontend/pages/home.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Home page of CleanOps.

Presents the application and lets visitors log in or create an account.
Logged in users get shortcuts to their projects and to a new audit.
"""


# -----------------------------------------------------------------------------
# frontend/pages/projects.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Page listing the projects of the logged in user.

Lets the user create a project, see its audits, start a new audit,
regenerate its secret key or delete it. A new secret key is displayed
only once.
"""


# -----------------------------------------------------------------------------
# frontend/pages/new_audit.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Page used to run a new audit.

The user uploads a code file and a dependency file, gives the secret key
of the project and chooses a quality gate. The request is signed with
HMAC before being sent. The certificate and the SBOM can then be
downloaded.
"""


# -----------------------------------------------------------------------------
# frontend/pages/audits.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Page listing the audits of the selected project.

Shows the details of an audit and lets the user download its certificate
(PDF) and its SBOM (JSON).
"""


# -----------------------------------------------------------------------------
# frontend/pages/public_key.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Public page displaying the public key used to sign the certificates.

Shows the key identifier (kid), the algorithm and the key in PEM format,
which can be downloaded to verify certificates offline.
"""


# -----------------------------------------------------------------------------
# frontend/pages/verify_certificate.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Public page used to verify a certificate.

The user pastes the signed certificate (JSON contained in the QR code of
the PDF) and the backend checks its signature.
"""


# -----------------------------------------------------------------------------
# frontend/utils/api_client.py
# -----------------------------------------------------------------------------
# [CONVERTED]
class APIClient:
    """
    Client for making authenticated HTTP requests to the backend API.

    Attributes
    ----------
    base_url : str
        Base URL of the API.
    timeout : int
        Default timeout for requests, in seconds.
    session : requests.Session
        Session used for connection pooling.

    Methods
    -------
    get(path, params=None, **kwargs)
        Send a GET request.
    post(path, json=None, data=None, **kwargs)
        Send a POST request.
    put(path, json=None, data=None, **kwargs)
        Send a PUT request.
    delete(path, **kwargs)
        Send a DELETE request.
    """

    def _get_headers(self) -> dict:
        """
        Generate the request headers, including the authentication token if present.

        Returns
        -------
        dict
            Request headers (``X-Auth-Token`` if the user is logged in).
        """
        ...

    # [NEW]
    def _request(self, method: str, path: str, **kwargs):
        """
        Send an HTTP request to the backend and normalize the response.

        Network errors are caught and returned with a status code of 0.

        Parameters
        ----------
        method : str
            HTTP method (``'GET'``, ``'POST'``, ``'PUT'`` or ``'DELETE'``).
        path : str
            Endpoint path.
        **kwargs : dict
            Additional arguments for ``requests.Session.request``. Also
            accepts ``sensitive`` (bool, if True the response body is not
            logged), ``headers`` and ``timeout``.

        Returns
        -------
        dict
            Dictionary with ``status_code`` (int), ``data`` (decoded JSON,
            text, or None for binary content) and ``content`` (raw bytes).
        """
        ...

    def get(self, path: str, params=None, **kwargs):
        """
        Send a GET request.

        Parameters
        ----------
        path : str
            Endpoint path.
        params : dict, optional
            Query parameters.
        **kwargs : dict
            Additional arguments for ``requests.request``.

        Returns
        -------
        dict
            Response dictionary (see ``_request``).
        """
        ...

    def post(self, path: str, json=None, data=None, **kwargs):
        """
        Send a POST request.

        Parameters
        ----------
        path : str
            Endpoint path.
        json : dict, optional
            JSON body of the request.
        data : dict or bytes, optional
            Form data or raw body.
        **kwargs : dict
            Additional arguments for ``requests.request``.

        Returns
        -------
        dict
            Response dictionary (see ``_request``).
        """
        ...

    def put(self, path: str, json=None, data=None, **kwargs):
        """
        Send a PUT request.

        Parameters
        ----------
        path : str
            Endpoint path.
        json : dict, optional
            JSON body of the request.
        data : dict or bytes, optional
            Form data or raw body.
        **kwargs : dict
            Additional arguments for ``requests.request``.

        Returns
        -------
        dict
            Response dictionary (see ``_request``).
        """
        ...

    def delete(self, path: str, **kwargs):
        """
        Send a DELETE request.

        Parameters
        ----------
        path : str
            Endpoint path.
        **kwargs : dict
            Additional arguments for ``requests.request``.

        Returns
        -------
        dict
            Response dictionary (see ``_request``).
        """
        ...


# -----------------------------------------------------------------------------
# frontend/utils/auth_guard.py
# -----------------------------------------------------------------------------
def check_authentification():
    """
    Check that the user is authenticated, otherwise redirect to the home page.

    Returns
    -------
    None
    """
    ...


# -----------------------------------------------------------------------------
# frontend/utils/env_variables.py
# -----------------------------------------------------------------------------
# Identique à backend utils/env_variables.py -> reprendre les docstrings
# de load_environment_variables, mask_value et display_values (Partie 4).


# -----------------------------------------------------------------------------
# frontend/utils/log_init.py
# -----------------------------------------------------------------------------
def initialize_logs(name: str):
    """
    Initialize logging from the ``logging_config.yml`` configuration file.

    Creates the ``logs`` folder at the root of the project if it does
    not exist.

    Parameters
    ----------
    name : str
        Name of the frontend application, written in the first log lines.

    Returns
    -------
    None
    """
    ...


def get_page_logger(page_name: str):
    """
    Track page navigation and return a dedicated logger for the page.

    Updates ``st.session_state`` (``last_navigated_page`` and ``logger``)
    when the page has changed.

    Parameters
    ----------
    page_name : str
        Name of the current page.

    Returns
    -------
    logging.Logger
        Logger of the current page.
    """
    ...


# -----------------------------------------------------------------------------
# frontend/utils/signature.py
# -----------------------------------------------------------------------------
def generate_signature(secret: bytes, project_id: int, code: bytes, dependency: bytes) -> str:
    """
    Generate the HMAC-SHA256 signature of a project submission.

    Identical to the backend's ``generate_signature``, but returns the
    signature encoded in Base64.

    Parameters
    ----------
    secret : bytes
        Secret HMAC key of the project.
    project_id : int
        Identifier of the project.
    code : bytes
        Content of the code file.
    dependency : bytes
        Content of the dependency file.

    Returns
    -------
    str
        Signature encoded in Base64.
    """
    ...


# =============================================================================
#  PARTIE 6 — tests/
# =============================================================================
#  Convention : les fonctions de test n'ont qu'une ligne de résumé (usage
#  courant avec numpydoc : un test ne prend pas de paramètres "métier" et ne
#  renvoie rien). Les helpers et les fixtures ont une docstring Numpy complète.


# -----------------------------------------------------------------------------
# tests/conftest.py
# -----------------------------------------------------------------------------
# [NEW]
"""
Shared pytest configuration: loads the environment variables before the tests.
"""


# -----------------------------------------------------------------------------
# tests/test_api/test_api_deps_dev.py
# -----------------------------------------------------------------------------
def make_response(data=None, status_code=200) -> MagicMock:
    """
    Build a fake ``requests.Response``.

    Parameters
    ----------
    data : dict, optional
        JSON returned by ``response.json()``. Empty dict if None.
    status_code : int, default 200
        HTTP status code of the response.

    Returns
    -------
    MagicMock
        Fake response.
    """
    ...


# [NEW]
def dep(name="requests", version="2.19.0") -> Dependency:
    """
    Build a Dependency for the tests.

    Parameters
    ----------
    name : str, default 'requests'
        Name of the dependency.
    version : str, default '2.19.0'
        Version of the dependency.

    Returns
    -------
    Dependency
        Dependency with ``id_dependency=1``.
    """
    ...


class TestCleanVersion:
    """Tests of ``API_DEPSDEV.clean_version``."""

    def test_extracts_first_version(self, raw, expected):
        """Extract the first exact version from a version specifier."""

    def test_returns_none_without_version(self, raw):
        """Return None when the specifier contains no version number."""


class TestToLicences:
    """Tests of ``API_DEPSDEV._to_licences``."""

    def test_known_licences_get_their_risk(self, name, risk):
        """Give each known licence the risk level defined in LICENCE_RISK."""

    def test_unknown_licence_gets_default_risk(self):
        """Give an unknown licence the default risk level ``'unknown'``."""

    def test_empty_list(self):
        """Return an empty list when no licence name is given."""

    def test_keeps_order_and_mixes_known_and_unknown(self):
        """Keep the order of the names, mixing known and unknown licences."""


class TestDefaultVersion:
    """Tests of ``API_DEPSDEV._default_version``."""

    def test_returns_default_version(self):
        """Return the version flagged ``isDefault``."""

    def test_no_default_version_flagged(self):
        """Return None when no version is flagged as default."""

    def test_no_versions_key(self):
        """Return None when the response has no ``versions`` key."""

    def test_unknown_package_returns_none(self):
        """Return None when deps.dev answers 404."""

    def test_http_error_is_propagated(self):
        """Propagate HTTP errors other than 404."""

    def test_calls_base_url_with_timeout(self):
        """Call the base URL of the package with a timeout."""


# -----------------------------------------------------------------------------
# tests/test_api/test_api_network.py
# -----------------------------------------------------------------------------
# [NEW] module docstring
"""
Integration tests calling the real OSV and deps.dev APIs (marker ``network``).
"""


def test_osv_real_call():
    """Find known vulnerabilities of requests 2.19.0 with the real OSV API."""


def test_depsdev_real_call():
    """Find the Apache-2.0 licence of requests 2.31.0 with the real deps.dev API."""


# -----------------------------------------------------------------------------
# tests/test_api/test_api_osv.py
# -----------------------------------------------------------------------------
def fake_cvss(score: float) -> MagicMock:
    """
    Build a fake CVSS class whose instances always return the given score.

    Parameters
    ----------
    score : float
        Score returned by ``scores()``.

    Returns
    -------
    MagicMock
        Fake CVSS class.
    """
    ...


# [NEW]
def osv_entry(osv_id: str, vector: str | None = None, aliases=None) -> dict:
    """
    Build a vulnerability entry as returned by the OSV API.

    Parameters
    ----------
    osv_id : str
        OSV identifier of the vulnerability.
    vector : str or None, optional
        CVSS v3 vector. No ``severity`` key is added if None.
    aliases : list of str, optional
        Aliases of the vulnerability (e.g. CVE identifiers).

    Returns
    -------
    dict
        OSV vulnerability entry.
    """
    ...


# [NEW]
def mock_post(data: dict) -> MagicMock:
    """
    Build a fake ``requests.post`` returning the given JSON.

    Parameters
    ----------
    data : dict
        JSON returned by ``response.json()``.

    Returns
    -------
    MagicMock
        Fake ``requests.post`` function.
    """
    ...


class TestGetSeverity:
    """Tests of ``API_OSV._get_severity``."""

    def test_severity_mapping(self, vector, expected):
        """Map real CVSS v3 vectors to the right severity level."""

    def test_threshold_boundaries(self, score, expected):
        """Respect the score boundaries between severity levels."""

    def test_each_cvss_version_uses_its_parser(self, cvss_type, cls_name):
        """Use the parser matching each CVSS version (v2, v3, v4)."""

    def test_skips_unknown_cvss_type(self):
        """Ignore entries with an unknown CVSS type."""

    def test_missing_severity_list(self):
        """Return None when the entry has no ``severity`` list."""

    def test_invalid_vector_returns_none(self):
        """Return None when the vector cannot be parsed."""

    def test_invalid_vector_then_valid_one(self):
        """Skip an unparsable entry and use the next one."""

    def test_real_cvss2_vector(self):
        """Read a real CVSS v2 vector."""

    def test_real_cvss4_vector(self):
        """Read a real CVSS v4 vector."""

    def test_first_readable_entry_wins(self):
        """Use the first readable entry when several are given."""


class TestToVulnerability:
    """Tests of ``API_OSV._to_vulnerability``."""

    def test_creates_correct_vulnerability_class(self, severity, expected_class):
        """Create the Vulnerability subclass matching the severity."""

    def test_sets_correct_fields(self):
        """Fill the fields of the vulnerability from the entry and the dependency."""

    def test_handles_missing_cve(self):
        """Set ``cve_id`` to None when no CVE alias exists."""

    def test_takes_first_cve_among_aliases(self):
        """Keep the first CVE found among the aliases."""

    def test_missing_aliases_key(self):
        """Set ``cve_id`` to None when the entry has no ``aliases`` key."""


class TestFindVulnerabilities:
    """Tests of ``API_OSV.find_vulnerabilities``."""

    def test_success_with_multiple_vulns(self):
        """Return one Vulnerability per OSV entry, with the right class."""

    def test_no_vulnerabilities(self):
        """Return an empty list when OSV finds no vulnerability."""

    def test_vuln_without_severity_is_skipped(self):
        """Skip the vulnerabilities without severity."""

    def test_sends_correct_request(self):
        """Send the expected payload to the OSV API."""

    def test_http_error_is_propagated(self):
        """Propagate HTTP errors."""

    def test_timeout_is_propagated(self):
        """Propagate timeouts."""

    def test_version_none_is_sent_as_null(self):
        """Send a missing version as ``null``."""

    def test_invalid_json_is_propagated(self):
        """Propagate the error raised by an invalid JSON response."""


# -----------------------------------------------------------------------------
# tests/test_business_object/test_qualitygatefactory.py
# -----------------------------------------------------------------------------
def test_returns_right_class(kind, cls):
    """Return the QualityGate class matching the requested type."""


def test_unknown_type_raises():
    """Raise a ValueError for an unknown type."""


def test_get_qualitygate_eco(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create an EcoQualityGate."""


def test_get_qualitygate_security(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create a SecurityQualityGate."""


def test_get_qualitygate_global(max_vuln, max_crit, max_carbon, max_energy, status):
    """Successfully create a GlobalQualityGate."""


def test_get_qualitygate_is_case_insensitive(qualitygate_type, expected_class):
    """Accept the type of the QualityGate whatever its case."""


def test_get_qualitygate_false_type(qualitygate_type):
    """Raise a ValueError when the type of the QualityGate is not valid."""


# -----------------------------------------------------------------------------
# tests/test_dao/test_audit_dao.py
# -----------------------------------------------------------------------------
def audit():
    """
    Create a sample audit containing two critical vulnerabilities.

    Returns
    -------
    Audit
        Audit with three vulnerabilities, two of them critical.
    """
    ...


def mock_db():
    """
    Create a mocked database connection and cursor.

    Returns
    -------
    tuple of MagicMock
        Fake ``DBConnection`` instance and fake cursor.
    """
    ...


def dao():
    """
    Create an AuditDao instance.

    Returns
    -------
    AuditDao
        DAO under test.
    """
    ...


def db_row(**overrides):
    """
    Create a sample row of ``audit_table``.

    Parameters
    ----------
    **overrides : dict
        Columns to override in the default row.

    Returns
    -------
    dict
        Database row.
    """
    ...


def test_row_to_audit():
    """Convert a database row into an Audit object."""


def test_create_success(dao, audit, mock_db):
    """Create an audit successfully."""


def test_create_quality_gate_object(dao, audit, mock_db):
    """Read the status from a quality gate object."""


def test_create_without_returned_row(dao, audit, mock_db):
    """Return False if INSERT returns no row."""


def test_create_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""


def test_find_by_id_success(dao, mock_db):
    """Return an audit when its ID exists."""


def test_find_by_id_not_found(dao, mock_db):
    """Return None when the audit does not exist."""


def test_find_by_id_database_error_is_reraised(dao):
    """Re-raise database errors."""


def test_find_all_success(dao, mock_db):
    """Return all audits from the database."""


def test_find_all_empty(dao, mock_db):
    """Return an empty list when there are no audits."""


def test_find_all_database_error_is_reraised(dao):
    """Re-raise database errors."""


def test_update_success(dao, audit, mock_db):
    """Return True when one audit is updated."""


def test_update_not_found(dao, audit, mock_db):
    """Return False when no audit is updated."""


def test_update_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""


def test_delete_success(dao, audit, mock_db):
    """Return True when an audit is deleted."""


def test_delete_not_found(dao, audit, mock_db):
    """Return False when no audit is deleted."""


def test_delete_database_error_is_reraised(dao, audit):
    """Re-raise database errors."""


def test_create_with_none_vulnerabilities(dao, audit, mock_db):
    """Create an audit when vulnerabilities is None."""


# -----------------------------------------------------------------------------
# tests/test_dao/test_project_dao.py
# -----------------------------------------------------------------------------
def cursor():
    """
    Give a fake database cursor for the tests.

    Yields
    ------
    MagicMock
        Fake cursor returned by ``DBConnection``.
    """
    ...


def user_dao():
    """
    Replace UserDao by a fake for the tests.

    Yields
    ------
    MagicMock
        Fake UserDao instance.
    """
    ...


def test_create_success(cursor):
    """Create the project and set its generated identifier."""


def test_create_returns_false_when_no_row(cursor):
    """Return False when the database returns no row (nothing created)."""


def test_create_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_find_by_id_found(cursor, user_dao):
    """Return the project when it is found."""


def test_find_by_id_not_found(cursor, user_dao):
    """Return None when the project is not found."""


def test_find_by_id_raises_on_db_error(cursor, user_dao):
    """Re-raise database errors."""


def test_list_all_project_returns_projects(cursor):
    """Return all the projects of the user."""


def test_list_all_project_empty(cursor):
    """Return an empty list when the user has no project."""


def test_list_all_project_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_update_success(cursor):
    """Return True when the project is successfully updated."""


def test_update_project_not_found(cursor):
    """Return False when the project to update does not exist."""


def test_update_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_delete_success(cursor):
    """Return True when the project is successfully deleted."""


def test_delete_project_not_found(cursor):
    """Return False when the project to delete does not exist."""


def test_delete_raises_on_db_error(cursor):
    """Re-raise database errors."""


# -----------------------------------------------------------------------------
# tests/test_dao/test_user_dao.py
# -----------------------------------------------------------------------------
def cursor():
    """
    Give a fake database cursor for the tests.

    Yields
    ------
    MagicMock
        Fake cursor returned by ``DBConnection``.
    """
    ...


# [NEW]
def test_create_success():
    """Create the user and set its generated identifier."""


def test_find_by_id_found(cursor):
    """Return the right user when the identifier exists."""


def test_find_by_id_not_found(cursor):
    """Return None when no user has this identifier."""


def test_find_by_id_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_find_all_found(cursor):
    """Return all the users of the database."""


def test_find_all_empty(cursor):
    """Return an empty list when there is no user."""


def test_find_all_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_update_success(cursor):
    """Return True when the user is successfully updated."""


def test_update_user_not_found(cursor):
    """Return False when the user to update does not exist."""


def test_update_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_delete_success(cursor):
    """Return True when the user is successfully deleted."""


def test_delete_user_not_found(cursor):
    """Return False when the user to delete does not exist."""


def test_delete_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_login_success(cursor):
    """Return the user when the credentials are valid."""


def test_login_wrong_credentials(cursor):
    """Return None when the password is wrong."""


def test_login_raises_on_db_error(cursor):
    """Re-raise database errors."""


def test_find_by_token_empty_token(cursor, token):
    """Return None without querying the database when the token is empty."""


def test_find_by_token_found(cursor):
    """Return the user owning the token."""


def test_find_by_token_not_found(cursor):
    """Return None when the token does not exist."""


def test_find_by_token_raises_on_db_error(cursor):
    """Re-raise database errors."""


# -----------------------------------------------------------------------------
# tests/test_service/test_audit_service.py
# -----------------------------------------------------------------------------
def test_create_successful():
    """Successfully create an Audit."""


def test_create_failed():
    """Fail to create an Audit because AuditDao().create returns False."""


def test_find_by_id_successful():
    """Successfully find the audit."""


def test_find_by_id_failed():
    """Fail to find the audit."""


def test_list_all_audit_successful():
    """Successfully list all the audits of a project."""


def test_list_all_audit_empty():
    """Return an empty list when the project has no audit."""


def test_run_audit_successful():
    """Successfully run an audit on a project."""


def test_run_audit_dao_create_fails():
    """Return None when AuditDao.create fails."""


# -----------------------------------------------------------------------------
# tests/test_service/test_eco_service.py
# -----------------------------------------------------------------------------
def code_file(source):
    """
    Build a real CodeFile, as expected by the service.

    Parameters
    ----------
    source : str or bytes
        Python source code. A ``str`` is dedented and encoded in UTF-8.

    Returns
    -------
    CodeFile
        Code file named ``'test.py'``.
    """
    ...


def summarize(antipattern):
    """
    Summarize an antipattern as a tuple.

    Parameters
    ----------
    antipattern : AntiPattern
        Antipattern to summarize.

    Returns
    -------
    tuple
        ``(type, line, detail)`` where detail is the depth for a
        NestedLoop and the function name for a RecursiveCall.
    """
    ...


def test_calculate_energy(source, input_size):
    """Return a positive float for the energy consumption."""


def test_calculate_energy_invalid_input_size(input_size):
    """Raise a ValueError when ``input_size`` is lower than 1."""


def test_calculate_carbon_default_intensity():
    """Use the default carbon intensity when none is given."""


def test_calculate_carbon_custom_intensity():
    """Use the carbon intensity given as argument."""


def test_calculate_carbon_zero_energy():
    """Return zero carbon for zero energy."""


def test_calculate_carbon_negative_intensity(intensity):
    """Raise a ValueError when the carbon intensity is negative."""


def test_calculate_carbon_rejects_invalid_input_size():
    """Raise a ValueError when ``input_size`` is invalid."""


def test_outest_loop(source, expected_lines):
    """Find only the loops that are not nested in another loop."""


def test_loop_depth(source, expected_depth):
    """Compute the loop nesting depth of a node."""


def test_is_recursive_call(call_source, function_name, expected):
    """Detect whether a call refers to the enclosing function."""


def test_detect_antipatterns(source, expected):
    """Detect the nested loops and the recursive calls of a code."""


def test_loop_length(source, expected):
    """Compute the number of iterations of a loop, or the default length."""


def test_loop_complexity(source, expected):
    """Compute the complexity of a loop, including its inner loops."""


def test_count_recursive_calls(source, expected):
    """Count the recursive calls of one execution of a function."""


def test_estimate_complexity(source, expected):
    """Estimate the complexity of a code."""


def test_estimate_complexity_returns_a_float():
    """Return the complexity as a float."""


def test_estimate_complexity_with_bytes_content():
    """Accept a code file whose content is bytes."""


# -----------------------------------------------------------------------------
# tests/test_service/test_project_service.py
# -----------------------------------------------------------------------------
def reset_dao_singleton():
    """
    Clear the ProjectDao singleton after each test.

    Yields
    ------
    None
    """
    ...


def test_upload_successful():
    """Successfully upload a Project."""


def test_upload_failed():
    """Fail to upload a Project because ProjectDao().create returns False."""


def test_find_by_id_successful():
    """Successfully find the Project related to the id."""


def test_find_by_id_failed():
    """Fail to find the Project because ProjectDao().find_by_id returns None."""


def test_list_all_project():
    """List all the projects of a user."""


def test_update_successful():
    """Successfully update the name of an existing Project."""


def test_update_failed():
    """Fail to update a Project because ProjectDao().update returns None."""


def test_delete_successful():
    """Successfully delete an existing Project."""


def test_delete_failed():
    """Fail to delete a Project because ProjectDao().delete returns False."""


# -----------------------------------------------------------------------------
# tests/test_service/test_qualitygate_service.py
# -----------------------------------------------------------------------------
def make_audit() -> Audit:
    """
    Build a minimal audit.

    Its content is irrelevant because ``evaluate()`` is mocked.

    Returns
    -------
    Audit
        Audit without vulnerabilities nor quality gate.
    """
    ...


def test_create_successful(qualitygate_type, expected_class):
    """Successfully create a QualityGate object."""


def test_create_delegates_to_factory():
    """Delegate the creation of the QualityGate to the factory."""


def test_create_false_type_qualitygate():
    """Raise a ValueError when the type of the QualityGate is not valid."""


def test_evaluate_successful(monkeypatch, qualitygate_type):
    """Set the status to 'Passed' when the project passes the QualityGate."""


def test_evaluate_failed(monkeypatch, qualitygate_type):
    """Set the status to 'Failed' when the project fails the QualityGate."""


# -----------------------------------------------------------------------------
# tests/test_service/test_sbom_service.py
# -----------------------------------------------------------------------------
def make_dependency(name, version=None):
    """
    Build a fake Dependency.

    ``generate()`` only reads ``.name`` and ``.version``.

    Parameters
    ----------
    name : str
        Name of the dependency.
    version : str, optional
        Version of the dependency.

    Returns
    -------
    types.SimpleNamespace
        Object with ``name`` and ``version`` attributes.
    """
    ...


def user():
    """
    Fictive user, because a project needs a user.

    Returns
    -------
    types.SimpleNamespace
        Fake user.
    """
    ...


def make_project(user):
    """
    Factory building a real project whose dependency file has the given name.

    Parameters
    ----------
    user : types.SimpleNamespace
        Owner of the project (fixture).

    Returns
    -------
    callable
        Function ``_make_project(filename='requirements.txt', name_project='demo')``
        returning a Project.
    """
    ...


def project(make_project):
    """
    Fictive Python project (``requirements.txt``).

    Parameters
    ----------
    make_project : callable
        Project factory (fixture).

    Returns
    -------
    Project
        Project named ``'demo'``.
    """
    ...


def file_service(monkeypatch):
    """
    Replace FileService inside ``sbom_service``.

    ``get_filename`` returns the name of the file; ``parse_dependencies``
    returns ``fake.parsed`` and records each call in ``fake.calls``.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Pytest fixture used to patch the module.

    Returns
    -------
    types.SimpleNamespace
        Object exposing ``parsed`` and ``calls``.
    """
    ...


def clean_version(monkeypatch):
    """
    Replace ``API_DEPSDEV.clean_version`` in ``sbom_service``.

    The fake removes the ``^``, ``~``, ``=`` and ``v`` prefixes and returns
    None for a range (e.g. ``'>=2.0'``) or a missing version.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Pytest fixture used to patch the module.

    Returns
    -------
    None
    """
    ...


def test_sbomfile_get_duty():
    """Return 'sbom' as the role of an SBOMFile."""


def test_generate_successful(project, file_service):
    """Generate a CycloneDX SBOM listing the normalized dependencies."""


def test_generate_failed():
    """Raise a ValueError when the project is None."""


def test_generate_parses_dependency_file_when_no_dependencies(project, file_service):
    """Parse the dependency file of the project when no dependency is given."""


def test_generate_with_given_dependencies(project, file_service):
    """Use the given dependencies, without duplicates and without parsing the file."""


def test_generate_uses_clean_version(project, file_service):
    """Clean the version of each dependency before building the purl."""


def test_generate_without_dependencies(project, file_service):
    """Generate an SBOM without components when there is no dependency."""


def test_generate_by_dependency_file_type(make_project, file_service, filename,
                                          dependencies, expected_purls):
    """Build the purls according to the type of the dependency file."""


def test_generate_unknown_file_defaults_to_pypi(make_project, file_service):
    """Use the pypi ecosystem for an unknown dependency file."""


def test_generate_with_vulnerabilities(project, file_service):
    """Add the vulnerabilities to the SBOM and link them to the affected components."""


def test_generate_vulnerability_on_unlisted_package(project, file_service):
    """Do not add ``affects`` for a vulnerability on a package not in the SBOM."""


def test_generate_severity_from_subclass(project, file_service, vulnerability_class, expected):
    """Deduce the severity from the class of each vulnerability."""


# -----------------------------------------------------------------------------
# tests/test_service/test_security_service.py
# -----------------------------------------------------------------------------
def test_detect_ecosystem_successful(name, type_file, expected):
    """Return the right OSV ecosystem for each supported dependency file."""


def test_detect_ecosystem_failed():
    """Raise a ValueError for an unsupported file (e.g. composer.json)."""


def test_find_vulnerabilities_aggregates_results_of_all_dependencies():
    """Combine the vulnerabilities found for each dependency into a single list."""


def test_find_vulnerabilities_calls_api_for_each_dependency_with_ecosystem():
    """Call the OSV API once per dependency, with the detected ecosystem."""


def test_find_vulnerabilities_no_dependencies_returns_empty_list():
    """Return an empty list and never call the API when there is no dependency."""


def test_unsupported_file_raises_and_skips_api():
    """Raise the error before any parsing or API call for an unsupported file."""


def test_api_error_propagates():
    """Propagate the errors raised by the OSV API."""


# -----------------------------------------------------------------------------
# tests/test_service/test_user_service.py
# -----------------------------------------------------------------------------
def test_created_successful():
    """Successfully create a User."""


def test_create_failed():
    """Fail to create a User because UserDao().create returns False."""


def test_find_by_id_successful():
    """Successfully find the user."""


def test_find_by_id_failed():
    """Fail to find the user."""


def test_update_successful():
    """Successfully update a user."""


def test_update_failed():
    """Fail to update a user because UserDao().update returns False."""


def test_delete_successful():
    """Successfully delete a user."""


def test_delete_failed():
    """Fail to delete a user because UserDao().delete returns False."""


def test_login_successful():
    """Successfully log in with a valid username and password."""


def test_login_failed():
    """Fail to log in because the credentials are wrong."""


def test_username_already_used_true():
    """Return True when a user with this username already exists."""


def test_username_already_used_false():
    """Return False when no user has this username."""


# -----------------------------------------------------------------------------
# tests/test_service/test_vulnerability_service.py
# -----------------------------------------------------------------------------
def test_count_critical_vulnerabilities():
    """Count only critical vulnerabilities."""


def test_count_empty_list():
    """Return zero for an empty list."""


def test_count_none():
    """Return zero when the list is None."""


def test_count_only_high_vulnerabilities():
    """Return zero if no critical vulnerability exists."""


def test_count_unexpected_objects():
    """Ignore objects that are not critical vulnerabilities."""


# -----------------------------------------------------------------------------
# tests/test_service/test_file_services/test_file_service.py
# -----------------------------------------------------------------------------
def test_get_filename_successful():
    """Build the filename from the name and the extension of the file."""


def test_get_filename_strips_leading_dot():
    """Do not duplicate the dot when the extension starts with one."""


def test_parse_dependencies_successful():
    """Delegate the parsing to the service matching the extension."""


def test_parse_dependencies_failed():
    """Raise a ValueError for an unsupported extension (e.g. .pdf)."""


# -----------------------------------------------------------------------------
# tests/test_service/test_file_services/test_json_service.py
# -----------------------------------------------------------------------------
def test_parse_dependencies_json_merges_dependencies_and_dev():
    """Combine ``dependencies`` and ``devDependencies`` into a single list."""


def test_parse_dependencies_json_without_dependencies():
    """Return an empty list for a JSON without dependency section."""


def test_parse_dependencies_json_invalid_raises():
    """Raise an error for a malformed JSON."""


# -----------------------------------------------------------------------------
# tests/test_service/test_file_services/test_toml_service.py
# -----------------------------------------------------------------------------
def test_toml_string_and_table_versions():
    """Read the version both as a string and as a table (``{ version = ... }``)."""


def test_toml_dependency_without_version():
    """Return None as version for a dependency without version (e.g. ``path``)."""


def test_toml_no_dependencies_section():
    """Return an empty list for a TOML file without ``[dependencies]`` section."""


# -----------------------------------------------------------------------------
# tests/test_service/test_file_services/test_txt_service.py
# -----------------------------------------------------------------------------
def test_parse_dependencies_txt_parse_pinned_and_unpinned():
    """Return the pinned version (``==``) and None for an unpinned dependency."""


def test_parse_dependencies_txt_ignores_comments_options_and_blank_lines():
    """Ignore comments, blank lines and options (``-r``, ``-e``)."""


def test_parse_dependencies_txt_handles_bom():
    """Read a UTF-8 file starting with a BOM."""


def test_parse_dependencies_txt_empty():
    """Return an empty list for an empty file."""


# -----------------------------------------------------------------------------
# tests/test_service/test_file_services/test_xml_service.py
# -----------------------------------------------------------------------------
def test_parse_dependencies_xml_parses_maven_dependency():
    """Name a Maven dependency ``groupId:artifactId`` and keep its version."""


def test_xml_invalid_raises():
    """Raise an error for a malformed XML."""


# -----------------------------------------------------------------------------
# tests/test_utils/test_security.py
# -----------------------------------------------------------------------------
class TestHashPassword:
    """Tests of ``hash_password``."""

    def test_known_value_without_salt(self):
        """Return the SHA-256 of the password when no salt is given."""

    def test_known_value_with_salt(self):
        """Return the SHA-256 of the password followed by the salt."""

    def test_default_salt_is_empty(self):
        """Use an empty salt by default."""

    def test_is_deterministic(self):
        """Return the same hash for the same inputs."""

    def test_different_salts_give_different_hashes(self):
        """Return different hashes for different salts."""

    def test_different_passwords_give_different_hashes(self):
        """Return different hashes for different passwords."""

    def test_output_format(self):
        """Return a 64-character hexadecimal string."""

    def test_empty_password(self):
        """Hash an empty password."""

    def test_unicode_password(self):
        """Hash a password containing unicode characters."""

    def test_concatenation_is_ambiguous(self):
        """Document the current behaviour: password and salt are simply concatenated."""


class TestVerifyToken:
    """Tests of ``verify_token``."""

    def test_missing_token_none(self):
        """Raise a 401 error when the token is None."""

    def test_missing_token_empty_string(self):
        """Raise a 401 error when the token is empty."""

    def test_missing_token_does_not_query_db(self, mock_dao_cls):
        """Do not query the database when the token is missing."""

    def test_invalid_token(self, mock_dao_cls):
        """Raise a 401 error when the token is unknown."""

    def test_valid_token_returns_user(self, mock_dao_cls):
        """Return the user owning a valid token."""


class TestGenerateSecretHMACKey:
    """Tests of ``generate_secret_HMAC_key``."""

    def test_returns_32_bytes(self):
        """Return a key of 32 bytes."""

    def test_keys_are_unique(self):
        """Return a different key at each call."""

    def test_uses_secrets_token_bytes(self, mock_tb):
        """Generate the key with ``secrets.token_bytes``."""


class TestEncodeSecretKey:
    """Tests of ``encode_secret_key``."""

    def test_bytes_are_base64_encoded(self):
        """Encode a bytes key in Base64."""

    def test_str_is_returned_unchanged(self):
        """Return a str key unchanged."""

    def test_empty_bytes(self):
        """Return an empty string for an empty key."""

    def test_roundtrip(self):
        """Get the original key back after decoding."""

    def test_generated_key_encoded_length(self):
        """Encode a 32-byte key into 44 characters."""


class TestGenerateSignature:
    """Tests of ``generate_signature``."""

    def test_returns_32_bytes(self):
        """Return a SHA-256 signature of 32 bytes."""

    def test_matches_manual_computation(self):
        """Match a signature computed manually."""

    def test_is_deterministic(self):
        """Return the same signature for the same inputs."""

    def test_different_secret_changes_signature(self):
        """Change the signature when the secret changes."""

    def test_any_input_change_changes_signature(self, project, code, dep):
        """Change the signature when any input changes."""

    def test_length_prefix_prevents_boundary_ambiguity(self):
        """Change the signature when bytes are moved from one field to another."""

    def test_field_order_matters(self):
        """Change the signature when the fields are swapped."""

    def test_empty_inputs(self):
        """Sign empty inputs."""

    def test_empty_inputs_differ_from_each_other_by_position(self):
        """Distinguish the same byte placed in different fields."""

    def test_large_inputs(self):
        """Sign large inputs."""

    def test_signature_can_be_verified_with_compare_digest(self):
        """Verify a signature with ``hmac.compare_digest``."""
