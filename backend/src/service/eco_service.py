import ast

from business_object.file.codefile import CodeFile

class EcoService:
    """Estimate the theoretical energy and carbon impact of Python code."""

    # Hypothetical reference machine
    CPU_POWER_W = 35.0
    OPERATIONS_PER_SECOND = 100_000_000

    # Illustrative electricity carbon intensity
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    @staticmethod
    def analyze_ast(code_file: CodeFile) -> dict:
        """Extract structural indicators from Python source code."""

        content = code_file.content

        if isinstance(content, bytes):
            content = content.decode("utf-8")

        if not isinstance(content, str):
            raise TypeError("CodeFile content must be str or bytes.")

        tree = ast.parse(content)

        loops = 0
        conditions = 0
        function_calls = 0
        operations = 0
        max_loop_depth = 0
        recursive_functions = []

        def visit(node, loop_depth=0, current_function=None):
            nonlocal loops, conditions, function_calls
            nonlocal operations, max_loop_depth

            if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                loops += 1
                loop_depth += 1
                max_loop_depth = max(max_loop_depth, loop_depth)

            if isinstance(node, ast.If):
                conditions += 1

            if isinstance(node, ast.Call):
                function_calls += 1

                if (
                    current_function is not None
                    and isinstance(node.func, ast.Name)
                    and node.func.id == current_function
                    and current_function not in recursive_functions
                ):
                    recursive_functions.append(current_function)

            if isinstance(
                node,
                (
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.Compare,
                    ast.BoolOp,
                    ast.AugAssign,
                ),
            ):
                operations += 1

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in node.body:
                    visit(child, loop_depth, node.name)
                return

            for child in ast.iter_child_nodes(node):
                visit(child, loop_depth, current_function)

        visit(tree)

        return {
            "ast_nodes": sum(1 for _ in ast.walk(tree)),
            "loops": loops,
            "nested_loops_depth": max_loop_depth,
            "conditions": conditions,
            "function_calls": function_calls,
            "operations": operations,
            "recursive_functions": recursive_functions,
        }

    def energy(self, code_file: CodeFile, input_size: int = 1000) -> float:
        """
        Estimate theoretical energy in kWh.

        The model uses AST indicators and a hypothetical reference CPU.
        Results are estimates, not physical measurements.
        """

        if input_size < 1:
            raise ValueError("input_size must be positive.")

        metrics = self.analyze_ast(code_file)

        # Estimate the number of operations for a reference input size.
        operations = metrics["operations"] + metrics["function_calls"]
        operations += metrics["ast_nodes"]

        if metrics["nested_loops_depth"] > 0:
            operations *= input_size ** metrics["nested_loops_depth"]

        if metrics["recursive_functions"]:
            operations *= input_size

        # Convert estimated operations to execution time.
        runtime_seconds = operations / self.OPERATIONS_PER_SECOND

        # E (kWh) = P (W) * t (s) / 3,600,000.
        energy_kwh = self.CPU_POWER_W * runtime_seconds / 3_600_000

        return energy_kwh

    def carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: float = None,
    ) -> float:
        """Convert estimated energy in kWh to emissions in gCO2e."""

        if energy_kwh < 0:
            raise ValueError("Energy cannot be negative.")

        if carbon_intensity_gco2e_per_kwh is None:
            carbon_intensity_gco2e_per_kwh = (
                self.CARBON_INTENSITY_GCO2E_PER_KWH
            )

        if carbon_intensity_gco2e_per_kwh < 0:
            raise ValueError("Carbon intensity cannot be negative.")

        return energy_kwh * carbon_intensity_gco2e_per_kwh
