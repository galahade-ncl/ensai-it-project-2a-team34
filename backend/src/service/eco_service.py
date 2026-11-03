import ast

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log


class EcoService:
    """
    Service responsible for AST analysis,
    energy estimation and carbon estimation.
    """

    # Garde les valeurs de ton projet si elles existent déjà.
    OPERATIONS_PER_SECOND = 1_000_000_000
    CPU_POWER_W = 65.0
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    @staticmethod
    def analyze_ast(code_file: "CodeFile") -> ast.Module:
        """
        Parse Python source code and return its AST.
        """

        content = code_file.content

        if isinstance(content, bytes):
            content = content.decode("utf-8")

        if not isinstance(content, str):
            raise TypeError(
                "CodeFile content must be str or bytes."
            )

        return ast.parse(content)

    @staticmethod
    def _extract_ast_metrics(tree: ast.Module) -> dict:
        """
        Extract complexity metrics from an AST.
        """

        class MetricsVisitor(ast.NodeVisitor):

            def __init__(self):
                self.loops = 0
                self.conditions = 0
                self.function_calls = 0
                self.operations = 0
                self.max_loop_depth = 0
                self.loop_depth = 0
                self.recursive_functions = []
                self.current_functions = []

            def _visit_loop(self, node):
                self.loops += 1
                self.loop_depth += 1

                self.max_loop_depth = max(
                    self.max_loop_depth,
                    self.loop_depth
                )

                self.generic_visit(node)
                self.loop_depth -= 1

            def visit_For(self, node):
                self._visit_loop(node)

            def visit_AsyncFor(self, node):
                self._visit_loop(node)

            def visit_While(self, node):
                self._visit_loop(node)

            def visit_If(self, node):
                self.conditions += 1
                self.generic_visit(node)

            def visit_IfExp(self, node):
                self.conditions += 1
                self.generic_visit(node)

            def visit_Call(self, node):
                self.function_calls += 1

                if (
                    self.current_functions
                    and isinstance(node.func, ast.Name)
                    and node.func.id == self.current_functions[-1]
                ):
                    function_name = self.current_functions[-1]

                    if function_name not in self.recursive_functions:
                        self.recursive_functions.append(function_name)

                self.generic_visit(node)

            def visit_BinOp(self, node):
                self.operations += 1
                self.generic_visit(node)

            def visit_UnaryOp(self, node):
                self.operations += 1
                self.generic_visit(node)

            def visit_Compare(self, node):
                self.operations += 1
                self.generic_visit(node)

            def visit_BoolOp(self, node):
                self.operations += 1
                self.generic_visit(node)

            def visit_AugAssign(self, node):
                self.operations += 1
                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                self.current_functions.append(node.name)
                self.generic_visit(node)
                self.current_functions.pop()

            def visit_AsyncFunctionDef(self, node):
                self.current_functions.append(node.name)
                self.generic_visit(node)
                self.current_functions.pop()

        visitor = MetricsVisitor()
        visitor.visit(tree)

        return {
            "ast_nodes": sum(1 for _ in ast.walk(tree)),
            "loops": visitor.loops,
            "nested_loops_depth": visitor.max_loop_depth,
            "conditions": visitor.conditions,
            "function_calls": visitor.function_calls,
            "operations": visitor.operations,
            "recursive_functions": visitor.recursive_functions,
        }

    def calculate_energy(
        self,
        code_file: "CodeFile",
        input_size: int = 1000
    ) -> float:
        """
        Estimate theoretical energy consumption in kWh.
        """

        if input_size < 1:
            raise ValueError("input_size must be positive.")

        # Build the AST
        tree = self.analyze_ast(code_file)

        # Extract AST metrics
        metrics = self._extract_ast_metrics(tree)

        # Estimate the number of operations
        operations = (
            metrics["operations"]
            + metrics["function_calls"]
            + metrics["ast_nodes"]
        )

        # Estimate nested loop complexity
        if metrics["nested_loops_depth"] > 0:
            operations *= (
                input_size ** metrics["nested_loops_depth"]
            )

        # Estimate recursive complexity
        if metrics["recursive_functions"]:
            operations *= input_size

        # Estimate execution time
        runtime_seconds = (
            operations / self.OPERATIONS_PER_SECOND
        )

        # Convert execution time into energy (kWh)
        energy_kwh = (
            self.CPU_POWER_W
            * runtime_seconds
            / 3_600_000
        )

        return energy_kwh

    def calculate_carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: Optional[float] = None,
    ) -> float:
        """
        Calculate carbon emissions in gCO2e.
        """

        if energy_kwh < 0:
            raise ValueError("Energy cannot be negative.")

        if carbon_intensity_gco2e_per_kwh is None:
            carbon_intensity_gco2e_per_kwh = (
                self.CARBON_INTENSITY_GCO2E_PER_KWH
            )

        if carbon_intensity_gco2e_per_kwh < 0:
            raise ValueError(
                "Carbon intensity cannot be negative."
            )

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
