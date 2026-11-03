import ast
from dataclasses import dataclass, field
from typing import Optional

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log


class _AnalysisVisitor(ast.NodeVisitor):
    """Single pass over the AST: collects metrics AND antipattern info."""

    def __init__(self):
        self.ast_nodes = 0
        self.loops = 0
        self.conditions = 0
        self.function_calls = 0
        self.operations = 0
        self.max_loop_depth = 0

        self._loop_depth = 0
        self._current_outer = None
        self.outer_loops = []        # [{"node": ..., "depth": ...}]
        self._functions = []         # stack of function names
        self.recursive_calls = []    # [(line, function_name)]

    def visit(self, node):
        self.ast_nodes += 1
        super().visit(node)

    def _visit_loop(self, node):
        self.loops += 1
        if self._loop_depth == 0:
            self._current_outer = {"node": node, "depth": 0}
            self.outer_loops.append(self._current_outer)
        self._loop_depth += 1
        self._current_outer["depth"] = max(
            self._current_outer["depth"], self._loop_depth
        )
        self.max_loop_depth = max(self.max_loop_depth, self._loop_depth)
        self.generic_visit(node)
        self._loop_depth -= 1

    visit_For = visit_AsyncFor = visit_While = _visit_loop

    def _visit_condition(self, node):
        self.conditions += 1
        self.generic_visit(node)

    visit_If = visit_IfExp = _visit_condition

    def _visit_operation(self, node):
        self.operations += 1
        self.generic_visit(node)

    visit_BinOp = visit_UnaryOp = visit_Compare = _visit_operation
    visit_BoolOp = visit_AugAssign = _visit_operation

    def _visit_function(self, node):
        self._functions.append(node.name)
        self.generic_visit(node)
        self._functions.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = _visit_function

    def visit_Call(self, node):
        self.function_calls += 1
        if self._functions and self._is_recursive_call(node, self._functions[-1]):
            self.recursive_calls.append((node.lineno, self._functions[-1]))
        self.generic_visit(node)

    @staticmethod
    def _is_recursive_call(call: ast.Call, function_name: str) -> bool:
        func = call.func
        if isinstance(func, ast.Name):
            return func.id == function_name
        return isinstance(func, ast.Attribute) and func.attr == function_name


@dataclass
class AstAnalysis:
    """Result of ONE pass over the code."""
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
        """Parse once, traverse once, return metrics + antipatterns."""
        visitor = _AnalysisVisitor()
        visitor.visit(self.parse(code_file))

        metrics = {
            "ast_nodes": visitor.ast_nodes,
            "loops": visitor.loops,
            "nested_loops_depth": visitor.max_loop_depth,
            "conditions": visitor.conditions,
            "function_calls": visitor.function_calls,
            "operations": visitor.operations,
            "recursive_functions": {name for _, name in visitor.recursive_calls},
        }

        antipatterns: list[AntiPattern] = [
            NestedLoop(
                line=outer["node"].lineno,
                description="Nested loop",
                depth=outer["depth"],
                id_antipattern=None,
            )
            for outer in visitor.outer_loops
            if outer["depth"] >= 2
        ]
        antipatterns += [
            RecursiveCall(
                line=line,
                description="Recursive_call",
                function_name=name,
                id_antipattern=None,
            )
            for line, name in visitor.recursive_calls
        ]
        return AstAnalysis(metrics=metrics, antipatterns=antipatterns)

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
