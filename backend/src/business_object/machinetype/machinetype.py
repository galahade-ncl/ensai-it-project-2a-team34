from enum import Enum


class MachineType(Enum):
    """
    Machine used to estimate the energy consumption and the carbon emission.

    Each member gives the three values of a machine, in this order:
    operations per second, power of the CPU (W) and carbon intensity of the
    electricity (gCO2e/kWh). REFERENCE must stay the first member: it is
    the default machine.

    Attributes
    ----------
    operations_per_second : int
        Number of operations executed per second by the CPU.
    cpu_power_w : float
        Power of the CPU (W).
    carbon_intensity_gco2e_per_kwh : float
        Carbon intensity of the electricity (gCO2e/kWh).
    """

    # NAME = (operations_per_second, cpu_power_w, carbon_intensity_gco2e_per_kwh)
    REFERENCE = (1_000_000_000, 65.0, 50.0)
    LAPTOP = (700_000_000, 25.0, 50.0)
    DESKTOP_HIGH_END = (1_500_000_000, 125.0, 50.0)
    RASPBERRY_PI = (200_000_000, 6.0, 50.0)
    REFERENCE_WORLD_MIX = (1_000_000_000, 65.0, 450.0)

    def __init__(self, operations_per_second, cpu_power_w, carbon_intensity_gco2e_per_kwh):
        self.operations_per_second = operations_per_second
        self.cpu_power_w = cpu_power_w
        self.carbon_intensity_gco2e_per_kwh = carbon_intensity_gco2e_per_kwh
