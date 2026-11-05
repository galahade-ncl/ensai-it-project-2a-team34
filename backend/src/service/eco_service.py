import ast
from dataclasses import dataclass, field

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log


@dataclass
class AstAnalysis:
    """Result of ONE analysis of the code (parsed once)."""

    metrics: dict
    antipatterns: list[AntiPattern] = field(default_factory=list)
    complexity: float = 0.0
    energy_kwh: float = 0.0
    carbon_gco2e: float = 0.0


class EcoService:
    """
    Service responsible for AST analysis,
    energy estimation and carbon estimation.
    """

    OPERATIONS_PER_SECOND = 1_000_000_000
    CPU_POWER_W = 65.0
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    LOOP_TYPES = (ast.For, ast.While)
    CONDITION_TYPES = (ast.If, ast.IfExp)
    OPERATION_TYPES = (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp, ast.AugAssign)

    @staticmethod
    def parse(code_file: CodeFile) -> ast.Module:
        """Parse Python source code and return its AST."""
        content = code_file.content
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        if not isinstance(content, str):
            raise TypeError("CodeFile content must be str or bytes.")
        return ast.parse(content)

    @log
    def analyze(self, code_file: CodeFile, input_size: int = 1000) -> AstAnalysis:
        """
        Full eco analysis of a code file (parsed only once):
        antipatterns, metrics, complexity, energy and carbon.
        """
        tree = self.parse(code_file)
        antipatterns = self._detect_antipatterns(tree)
        metrics = self._extract_metrics(tree, antipatterns)
        energy = self._calculate_energy(metrics, input_size)

        return AstAnalysis(
            metrics=metrics,
            antipatterns=antipatterns,
            complexity=self._estimate_complexity(tree),
            energy_kwh=energy,
            carbon_gco2e=self._calculate_carbon(energy),
        )

    def _extract_metrics(self, tree: ast.Module, antipatterns: list[AntiPattern]) -> dict:
        """
        Simple counts with ONE ast.walk. Loop depth and recursive functions
        are reused from the antipatterns (not recomputed).
        """
        nodes = list(ast.walk(tree))
        loops = sum(isinstance(n, self.LOOP_TYPES) for n in nodes)

        # NestedLoop antipatterns cover every outermost loop of depth >= 2,
        # so the max depth is there; otherwise it is 1 if a loop exists, else 0.
        nested_depths = [a.depth for a in antipatterns if isinstance(a, NestedLoop)]
        if nested_depths:
            max_loop_depth = max(nested_depths)
        else:
            max_loop_depth = 1 if loops > 0 else 0

        return {
            "ast_nodes": len(nodes),
            "loops": loops,
            "nested_loops_depth": max_loop_depth,
            "conditions": sum(isinstance(n, self.CONDITION_TYPES) for n in nodes),
            "function_calls": sum(isinstance(n, ast.Call) for n in nodes),
            "operations": sum(isinstance(n, self.OPERATION_TYPES) for n in nodes),
            "recursive_functions": {
                a.function_name for a in antipatterns if isinstance(a, RecursiveCall)
            },
        }

    @log
    def calculate_energy(self, code_file: CodeFile, input_size: int = 1000) -> float:
        """Estimate theoretical energy consumption in kWh of a code file."""
        tree = self.parse(code_file)
        metrics = self._extract_metrics(tree, self._detect_antipatterns(tree))
        return self._calculate_energy(metrics, input_size)

    def _calculate_energy(self, metrics: dict, input_size: int = 1000) -> float:
        if input_size < 1:
            raise ValueError("input_size must be positive.")
        operations = metrics["operations"] + metrics["function_calls"] + metrics["ast_nodes"]
        if metrics["nested_loops_depth"] > 0:
            operations *= input_size ** metrics["nested_loops_depth"]
        if metrics["recursive_functions"]:
            operations *= input_size

        runtime_seconds = operations / self.OPERATIONS_PER_SECOND
        return self.CPU_POWER_W * runtime_seconds / 3_600_000

    @log
    def calculate_carbon(
        self,
        code_file: CodeFile,
        input_size: int = 1000,
        carbon_intensity_gco2e_per_kwh: float | None = None,
    ) -> float:
        """Calculate carbon emissions in gCO2e of a code file."""
        energy_kwh = self.calculate_energy(code_file, input_size)
        return self._calculate_carbon(energy_kwh, carbon_intensity_gco2e_per_kwh)

    def _calculate_carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: float | None = None,
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
    def detect_antipatterns(self, code_file: CodeFile) -> list[AntiPattern]:
        """
        Detect all the antipatterns in a Python code
        Args:
            code_file (CodeFile) : The code to analyse
        Returns:
            A list of the Antipatterns of the code
        """
        return self._detect_antipatterns(self.parse(code_file))

    @log
    def _detect_antipatterns(self, tree: ast.Module) -> list[AntiPattern]:
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

    DEFAULT_LOOP_LENGTH = 10
    DEFAULT_RECURSION_DEPTH = 10

    @staticmethod
    def _loop_length(node: ast.stmt) -> int:
        """
        Calculate the length of a loop
        Args:
            node (ast.stmt): A for or while loop
        Returns:
            int: The length of the loop, or DEFAULT_LOOP_LENGTH if it cannot be known
        """
        if isinstance(node, ast.For):
            iteration = node.iter

            if isinstance(
                iteration, (ast.List, ast.Tuple, ast.Set)
            ):  # for i in [1, 2, 3] / for i in (1, 2, 3) / for i in {1, 2, 3}
                return len(iteration.elts)

            if isinstance(iteration, ast.Constant) and isinstance(
                iteration.value, (str, bytes)
            ):  # for i in "abc"
                return len(iteration.value)

            if (
                isinstance(iteration, ast.Call)
                and isinstance(iteration.func, ast.Name)
                and iteration.func.id == "range"
            ):  # for i in range (3) / for i in range (2, 10, 2)
                try:
                    values = [ast.literal_eval(arg) for arg in iteration.args]
                    return len(range(*values))
                except (ValueError, TypeError):  # for i in range (n)
                    pass

        # Cannot know the length : for val in values / while
        return EcoService.DEFAULT_LOOP_LENGTH

    @staticmethod
    def _loop_complexity(node: ast.stmt) -> int:
        """
        Calculate the complexity of a loop
        Args:
            node (ast.stmt): A loop
        Returns:
            The complexity of the loop
        """
        complexity = EcoService._loop_length(node)

        if EcoService._loop_depth(node) >= 2:
            inner_complexity = 0
            for inner_loop in EcoService._outest_loop(node):
                inner_complexity += EcoService._loop_complexity(inner_loop)
            return complexity * inner_complexity

        return complexity

    @staticmethod
    def _count_recursive_calls(node: ast.AST, function_name: str) -> int:
        """
        Count the recursive calls made by one execution of a function, a call inside a loop being counted once per iteration
        Args:
            node (ast.AST): The function to analyse
            function_name (str): The name of the function
        Returns:
            int: The number of recursive calls
        """
        total = 0

        for child in ast.iter_child_nodes(node):
            count = EcoService._count_recursive_calls(child, function_name)

            if isinstance(child, ast.Call) and EcoService._is_recursive_call(child, function_name):
                count += 1

            if isinstance(child, (ast.For, ast.While)):
                count *= EcoService._loop_length(child)

            total += count

        return total

    @log
    def estimate_complexity(self, codefile: CodeFile) -> float:
        """
        Estimate the complexity of a Python code
        Args:
            codefile (CodeFile) : The code to be estimate
        Returns:
            float : complexity of the code
        """
        return self._estimate_complexity(self.parse(codefile))

    @log
    def _estimate_complexity(self, tree: ast.Module) -> float:
        """
        Estimate the complexity of a Python code
        Args:
            codefile (CodeFile) : The code to be estimate
        Returns:
            float : complexity of the code
        """

        complexity = 1

        # Complexity of all the loops
        for loop in EcoService._outest_loop(tree):
            complexity += EcoService._loop_complexity(loop)

        # Complexity of all the recursive calls
        for function in ast.walk(tree):
            if not isinstance(function, ast.FunctionDef):
                continue

            calls = EcoService._count_recursive_calls(function, function.name)
            if calls != 0:
                executions = sum(
                    calls**level for level in range(EcoService.DEFAULT_RECURSION_DEPTH + 1)
                )

                one_execution = 1
                for loop in EcoService._outest_loop(function):
                    one_execution += EcoService._loop_complexity(loop)
                    complexity += one_execution * (executions - 1)

        return float(complexity)
