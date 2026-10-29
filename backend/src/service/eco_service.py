import ast

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log


class EcoService:
    """
    Service that handles business logic related to the eco analyse of a Python code
    """

    """Service for estimating the energy consumption and carbon emissions of Python code."""

    # ---------------------
    # Partie Thomas
    # ---------------------

    # Hypotheses for a theoretical estimation model
    CPU_POWER_W = 35.0
    OPERATIONS_PER_SECOND = 100_000_000
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    @staticmethod
    def analyze_ast(code_file: CodeFile) -> dict:
        """Analyze Python source code using its Abstract Syntax Tree (AST)."""
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

    def calculate_energy(self, code_file: CodeFile, input_size: int = 1000) -> float:
        """Estimate theoretical energy consumption in kWh."""
        if input_size < 1:
            raise ValueError("input_size must be positive.")

        metrics = self.analyze_ast(code_file)

        # Estimate the number of operations
        operations = metrics["operations"] + metrics["function_calls"] + metrics["ast_nodes"]

        # Apply a rough estimate based on nested loop depth
        if metrics["nested_loops_depth"] > 0:
            operations *= input_size ** metrics["nested_loops_depth"]

        # Apply an additional estimate when recursive functions are detected
        if metrics["recursive_functions"]:
            operations *= input_size

        # Convert estimated execution time into energy in kWh
        runtime_seconds = operations / self.OPERATIONS_PER_SECOND
        energy_kwh = self.CPU_POWER_W * runtime_seconds / 3_600_000

        return energy_kwh

    def calculate_carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: float = None,
    ) -> float:
        """Calculate carbon emissions in gCO2e."""
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
