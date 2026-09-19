from business_object.qualitygate import QualityGate
from business_object.project import Project

# Initialization
# initialize_logs("Webservice")
# load_environment_variables()
# display_values()

qualitygate = QualityGate(2, 0, 50, "Good")
project = Project("Test de Projet", "Psyduck", "fichier code", "fichier dépendance", "HMAC")
print(qualitygate)
print(project)
