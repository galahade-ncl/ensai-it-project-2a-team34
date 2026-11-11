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
    sbom : SBOM
        Software Bill of Materials, the inventory of components used
        by the project.
    quality_gate : QualityGate
        Quality gate associated with the project.
    certificate : CertificateFile
        Certificate associated with the audit.

    Methods
    -------
    __str__()
        Return a string representation of the audit.
    """

    def __init__(
        self,
        id_project,
        date,
        vulnerabilities,
        licenses,
        anti_patterns,
        complexity,
        energy_consumption_kwh,
        carbon_emission_gco2e,
        sbom,
        quality_gate,
        certificate,
        id_audit=None
    ) -> None:
        self.id_audit = id_audit
        self.id_project = id_project
        self.date = date
        self.vulnerabilities = vulnerabilities
        self.licenses = licenses
        self.anti_patterns = anti_patterns
        self.complexity = complexity
        self.energy_consumption_kwh = energy_consumption_kwh
        self.carbon_emission_gco2e = carbon_emission_gco2e
        self.sbom = sbom
        self.quality_gate = quality_gate
        self.certificate = certificate

    def __str__(self):
        """
        Return a string representation of the audit.

        Returns
        -------
        str
            String showing the project identifier and the energy
            consumption of the audit.
        """
        return f"Audit: Audit of the project {self.id_project}. It consume {self.energy_consumption_kwh} kwh."
