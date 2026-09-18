from business_object.qualitygate import QualityGate

# Initialization
#initialize_logs("Webservice")
#load_environment_variables()
#display_values()

qualitygate = QualityGate(2, 0, 50, "Good")
print(qualitygate)
