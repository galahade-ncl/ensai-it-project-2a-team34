from business_object.project import Project
from business_object.qualitygate.globalqualitygate import GlobalQualityGate

# Initialization
# initialize_logs("Webservice")
# load_environment_variables()
# display_values()

qualitygate = GlobalQualityGate(2, 0, 50, 200, "Good")
project = Project("Test de Projet", "Psyduck", "fichier code", "fichier dépendance", "HMAC")
print(qualitygate)
print(project)

print(qualitygate.max_vulnerabilities)
