from business_object.audit import Audit


class EcoQualityGate:
    def __init__(self, id_quality_gate, max_carbon_emission, max_energy_consumption, status):
        self.id_quality_gate = id_quality_gate
        self.max_carbon_emission = max_carbon_emission
        self.max_energy_consumption = max_energy_consumption
        self.status = status

    def evaluate(self, audit: Audit) -> bool:
        if audit.carbon_emission_gco2e > self.max_carbon_emission:
            return ("The carbon emission is too high")

        if audit.energy_consumption_kwh > self.max_energy_consumption:
            return ("The energy consumption is too high")
