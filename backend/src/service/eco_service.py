import ast

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log
from typing import Optional

class EcoService:
    """Service responsible for energy and carbon estimation."""

    OPERATIONS_PER_SECOND = 1_000_000_000
    CPU_POWER_W = 65.0
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    def calculate_energy(self, metrics: dict, input_size: int = 1000) -> float:
        """Estimate theoretical energy consumption in kWh."""
        if input_size < 1:
            raise ValueError("input_size must be positive.")

        operations = (
            metrics["operations"] + metrics["function_calls"] + metrics["ast_nodes"]
        )
        if metrics["nested_loops_depth"] > 0:
            operations *= input_size ** metrics["nested_loops_depth"]
        if metrics["recursive_functions"]:
            operations *= input_size

        runtime_seconds = operations / self.OPERATIONS_PER_SECOND
        return self.CPU_POWER_W * runtime_seconds / 3_600_000

    def calculate_carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: Optional[float] = None,
    ) -> float:
        if energy_kwh < 0:
            raise ValueError("Energy cannot be negative.")
        if carbon_intensity_gco2e_per_kwh is None:
            carbon_intensity_gco2e_per_kwh = self.CARBON_INTENSITY_GCO2E_PER_KWH
        if carbon_intensity_gco2e_per_kwh < 0:
            raise ValueError("Carbon intensity cannot be negative.")
        return energy_kwh * carbon_intensity_gco2e_per_kwh
        
    # ---------------------
    # Partie Annabelle
    # ---------------------

    @staticmethod
    def _outest_loop(tree: ast.AST) -> list[ast.stmt]:
        """
        Find all the loop that is not nested in an other loop
        Args:
            tree (ast.AST) : The AST of the code
        Returns:
            A list of loop
        """
        loop_type = (ast.For, ast.While)
        loops = []

        for child in ast.iter_child_nodes(tree):
            if isinstance(child, loop_type):
                loops.append(child)
            else:
                loops.extend(EcoService._outest_loop(child))

        return loops

    @staticmethod
    def _loop_depth(node: ast.AST) -> int:
        """
        Depth of a node
        Args:
            node (ast.AST) : The node
        Returns:
            An integer that is the depth of the node
        """
        loop_type = (ast.For, ast.While)
        depth = 0
        for child in ast.iter_child_nodes(node):
            child_depth = EcoService._loop_depth(child)
            if child_depth > depth:
                depth = child_depth

        return depth + isinstance(node, loop_type)

    @staticmethod
    def _is_recursive_call(call: ast.Call, function_name: str) -> bool:
        """
        Verify if call is a recursive call
        Args:
            call (ast.Call) : A call inside a function named function_name
            function_name (str) : The name of the function
        Returns:
            True if the call is refered to the function named function_name
        """
        func = call.func

        if isinstance(func, ast.Name):
            return func.id == function_name
        return isinstance(func, ast.Attribute) and func.attr == function_name

    @log
    def detect_antipatterns(self, tree: ast.Module) -> list[AntiPattern]:
        """
        Detect all the antipatterns in a Python code
        Args:
            tree (ast.Module) : The AST (Abstract Syntax Tree) of the code
        Returns:
            A list of the Antipatterns of the code
        """
        antipatterns = []

        # Nested loop
        for loop in EcoService._outest_loop(tree):
            depth = EcoService._loop_depth(loop)
            if depth >= 2:
                antipatterns.append(
                    NestedLoop(
                        line=loop.lineno,
                        description="Nested loop",
                        depth=depth,
                        id_antipattern=None,
                    )
                )

        # Recursive call
        for func in ast.walk(tree):
            if isinstance(func, ast.FunctionDef):
                for node in ast.walk(func):
                    if isinstance(node, ast.Call) and EcoService._is_recursive_call(
                        node, func.name
                    ):
                        antipatterns.append(
                            RecursiveCall(
                                line=node.lineno,
                                description="Recursive_call",
                                function_name=func.name,
                                id_antipattern=None,
                            )
                        )
        return antipatterns
