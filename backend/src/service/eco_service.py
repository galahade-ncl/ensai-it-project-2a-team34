import ast
import operator
from dataclasses import dataclass, field
from typing import Optional

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
    def analyze(self, code_file: CodeFile) -> AstAnalysis:
        """
        Parse once, detect the antipatterns once, and derive the metrics
        (loop depth, recursion) from them instead of recomputing them.
        """
        tree = self.parse(code_file)
        antipatterns = self.detect_antipatterns(tree)
        metrics = self._extract_metrics(tree, antipatterns)
        return AstAnalysis(metrics=metrics, antipatterns=antipatterns)

    def _extract_metrics(
        self, tree: ast.Module, antipatterns: list[AntiPattern]
    ) -> dict:
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

    def calculate_energy(self, metrics: dict, input_size: int = 1000) -> float:
        """Estimate theoretical energy consumption in kWh from metrics."""
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



    DEFAULT_LOOP_LENGTH = 10
    DEFAULT_RECURSION_DEPTH = 10

    _BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    @staticmethod
    def _evaluate_expression(node: ast.expr, variables: Optional[dict] = None) -> Optional[int]:

        variables = variables or {}

        # Constantes : 3, 10, etc.
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                return node.value

            if isinstance(node.value, (str, bytes)):
                return len(node.value)

        # Variables : n
        if isinstance(node, ast.Name):
            return variables.get(node.id)

        # Opérations unaires : -n, +n
        if isinstance(node, ast.UnaryOp):
            value = EcoService._evaluate_expression(node.operand, variables)

            if value is None:
                return None

            if isinstance(node.op, ast.USub):
                return -value

            if isinstance(node.op, ast.UAdd):
                return value

        # Opérations binaires : n + 2, n * 2, etc.
        if isinstance(node, ast.BinOp):
            left = EcoService._evaluate_expression(node.left, variables)
            right = EcoService._evaluate_expression(node.right, variables)

            if left is None or right is None:
                return None

            try:
                if isinstance(node.op, ast.Add):
                    return left + right

                if isinstance(node.op, ast.Sub):
                    return left - right

                if isinstance(node.op, ast.Mult):
                    return left * right

                if isinstance(node.op, ast.FloorDiv):
                    return left // right if right != 0 else None

                if isinstance(node.op, ast.Mod):
                    return left % right if right != 0 else None

            except (ArithmeticError, OverflowError):
                return None

        # len([1, 2, 3]), len("abc"), len(my_list)
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "len"
                and len(node.args) == 1
                and not node.keywords
            ):
                arg = node.args[0]

                if isinstance(arg, (ast.List, ast.Tuple, ast.Set)):
                    return len(arg.elts)

                if isinstance(arg, ast.Constant) and isinstance(
                    arg.value, (str, bytes)
                ):
                    return len(arg.value)

                if isinstance(arg, ast.Name):
                    value = variables.get(arg.id)

                    if isinstance(value, (list, tuple, set, str, bytes)):
                        return len(value)

                    if isinstance(value, int):
                        # L'environnement peut aussi stocker directement
                        # la longueur d'une collection.
                        return value

        return None


    @staticmethod
    def _loop_length(node: ast.stmt, variables: Optional[dict] | None) -> int:
        """
        Calculate the length of a loop
        Args:
            node (ast.stmt): A for or while loop
        Returns:
            int: The length of the loop, or DEFAULT_LOOP_LENGTH if it cannot be known
        """
        variables = variables or {}

        if isinstance(node, ast.For):
            iteration = node.iter

            if isinstance(iteration, (ast.List, ast.Tuple, ast.Set)): # for i in [1, 2, 3] / for i in (1, 2, 3) / for i in {1, 2, 3}
                return len(iteration.elts)

            if isinstance(iteration, ast.Constant) and isinstance(iteration.value, (str, bytes)): # for i in "abc"
                return len(iteration.value)

            if (
                isinstance(iteration, ast.Call)
                and isinstance(iteration.func, ast.Name)
                and iteration.func.id == "range"
            ): # for i in range (3) / for i in range (2, 10, 2)
                if not 1 <= len(iteration.args) <=3 or iteration.keywords: # for i in range (1, 2, 3, 4)
                    return 0

                values = [EcoService._evaluate_expression(arg, variables) for arg in iteration.args]
                
                if any (value is None for value in values):
                    return EcoService.DEFAULT_LOOP_LENGTH
                try:
                    return len(range(*values))
                
                except (ValueError, TypeError): # for i in range (n)
                    return 0

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
        tree = ast.parse(codefile.content)

        complexity = 1

        # Complexity of all the loops
        for loop in EcoService._outest_loop(tree):
            complexity += EcoService._loop_complexity(loop)

        # Complexity of all the recursive calls
        for function in ast.walk(tree):
            if not isinstance(function, ast.FunctionDef):
                continue

            calls = EcoService._count_recursive_calls(function, function.name)
            if calls == 0:
                continue

            executions = sum(
                calls**level for level in range(EcoService.DEFAULT_RECURSION_DEPTH + 1)
            )

            one_execution = 1
            for loop in EcoService._outest_loop(function):
                one_execution += EcoService._loop_complexity(loop)

            complexity += one_execution * (executions - 1)

        return float(complexity)

