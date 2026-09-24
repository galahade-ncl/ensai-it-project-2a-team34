class Audit:
    ''' Class representing the audit of a project
        Attributes:
            id_audit (int): The unique identifier of the audit
            id_project (int): The unique identifier of the project from which this audit is linked
            date (datetime): The date the audit was created
            vulnerabilities (list[Vulnerability]): The list of vulnerabilities found in the dependancies of the project
            licenses (list[License]): The list of licence used by the code of the project
            anti_patterns (list[AntiPattern]): The list of antipatterns found in the project
            complexity (float): The complexity of the code
            energy_consumption_kwh (float): The energy consumption of the code (kwh)
            carbon_emission_gco2e (float): The carbon emission of the code
            sbom (SBOM): Software Bill of Materials, the inventory of components used for the project
            quality_gate (QualityGate): The quality gate associed to the project
                    HMACkey (hmac.HMAC): The HMACkey associated with the project
    '''

    def __init__(
        self,
        id_audit,
        id_project,
        date,
        vulnerabilities,
        licenses,
        anti_patterns,
        complexity,
        energy_consumption_kwh,
        carbon_emission_gco2e,
        sbom,
        quality_gate
    ):
        self.id_audit = id_audit
        self.id_project = id_project
        self.date = date
        self.vulnerabilities  =vulnerabilities
        self.licenses = licenses
        self.anti_patterns = anti_patterns
        self.complexity = complexity
        self.energy_consumption_kwh = energy_consumption_kwh
        self.carbon_emission_gco2e = carbon_emission_gco2e
        self. sbom = sbom
        self.quality_gate = quality_gate

    def __str__(self):
        """Returns a string representation of the audit
        """
        