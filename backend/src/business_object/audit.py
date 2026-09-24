class Audit:
    ''' Class representing the audit of a project
        Attributes:
            id_audit (int): The unique identifier of the audit
            id_project (int): The unique identifier of the project from which this audit is linked
            date (datetime): The date the audit was created
            vulnerabilities (list[Vulnerability]): The list of vulnerabilities found in the dependancies of the project
            licenses (list[License]): The list of licence used by the code of the project
            anti_patterns (list[AntiPattern]): The list of antipatterns found in the project
            complexity (float): 
            codefile (CodeFile): the code file of the project
            dependencyfile (DependencyFile): the dependency file of the project
            HMACkey (hmac.HMAC): The HMACkey associated with the project
    '''