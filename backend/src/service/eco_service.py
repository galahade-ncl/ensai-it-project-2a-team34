import ast
from dataclasses import dataclass, field

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from utils.log_utils import log


@dataclass
class AstAnalysis:
    """
    Result of ONE analysis of the code (parsed once).

    Attributes
    ----------
    metrics : dict
        Metrics extracted from the AST.
    antipatterns : list of AntiPattern
        Antipatterns detected in the code.
    complexity : float
        Estimated complexity of the code.
    energy_kwh : float
        Estimated energy consumption (kWh).
    carbon_gco2e : float
        Estimated carbon emission (gCO2e).
    """

    metrics: dict
    antipatterns: list[AntiPattern] = field(default_factory=list)
    complexity: float = 0.0
    energy_kwh: float = 0.0
    carbon_gco2e: float = 0.0


class EcoService:
    """
    Service responsible for AST analysis, energy estimation and carbon
    estimation.

    Attributes
    ----------
    OPERATIONS_PER_SECOND : int
        Number of operations executed per second by the reference CPU.
    CPU_POWER_W : float
        Power of the reference CPU (W).
    CARBON_INTENSITY_GCO2E_PER_KWH : float
        Default carbon intensity of electricity (gCO2e/kWh).
    DEFAULT_LOOP_LENGTH : int
        Number of iterations assumed when the length of a loop is unknown.
    DEFAULT_RECURSION_DEPTH : int
        Recursion depth assumed for recursive functions.
    """

    OPERATIONS_PER_SECOND = 1_000_000_000
    CPU_POWER_W = 65.0
    CARBON_INTENSITY_GCO2E_PER_KWH = 50.0

    LOOP_TYPES = (ast.For, ast.While)
    CONDITION_TYPES = (ast.If, ast.IfExp)
    OPERATION_TYPES = (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp, ast.AugAssign)

    @staticmethod
    def parse(code_file: CodeFile) -> ast.Module:
        """
        Parse Python source code and return its AST.

        Parameters
        ----------
        code_file : CodeFile
            Code file to parse. Its content may be ``str`` or ``bytes``
            (decoded as UTF-8).

        Returns
        -------
        ast.Module
            Abstract Syntax Tree of the code.

        Raises
        ------
        TypeError
            If the content of the file is neither ``str`` nor ``bytes``.
        SyntaxError
            If the code is not valid Python.
        """
        content = code_file.content
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        if not isinstance(content, str):
            raise TypeError("CodeFile content must be str or bytes.")
        return ast.parse(content)

    @log
    def analyze(self, code_file: CodeFile, input_size: int = 1000) -> AstAnalysis:
        """
        Run the full eco analysis of a code file.

        The code is parsed only once, then used to compute the antipatterns,
        the metrics, the complexity, the energy and the carbon emission.

        Parameters
        ----------
        code_file : CodeFile
            Code file to analyse.
        input_size : int, default 1000
            Assumed size of the input data, used to estimate the energy.

        Returns
        -------
        AstAnalysis
            Result of the analysis.
        """
        tree = self.parse(code_file)
        antipatterns = self.detect_antipatterns(tree)
        metrics = self._extract_metrics(tree, antipatterns)
        energy = self.calculate_energy(metrics, input_size)

        return AstAnalysis(
            metrics=metrics,
            antipatterns=antipatterns,
            complexity=self.estimate_complexity(tree),
            energy_kwh=energy,
            carbon_gco2e=self.calculate_carbon(energy),
        )

    def _extract_metrics(self, tree: ast.Module, antipatterns: list[AntiPattern]) -> dict:
        """
        Extract simple counts from the AST with a single ``ast.walk``.

        Loop depth and recursive functions are reused from the antipatterns
        (not recomputed).

        Parameters
        ----------
        tree : ast.Module
            AST of the code.
        antipatterns : list of AntiPattern
            Antipatterns already detected in the code.

        Returns
        -------
        dict
            Metrics: ``ast_nodes``, ``loops``, ``nested_loops_depth``,
            ``conditions``, ``function_calls``, ``operations`` and
            ``recursive_functions``.
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
        """
        Estimate the energy consumption of the code.

        The number of operations is multiplied by ``input_size`` raised to
        the loop nesting depth, and once more if there is recursion.

        Parameters
        ----------
        metrics : dict
            Metrics returned by ``_extract_metrics``.
        input_size : int, default 1000
            Assumed size of the input data.

        Returns
        -------
        float
            Estimated energy consumption (kWh).

        Raises
        ------
        ValueError
            If ``input_size`` is lower than 1.
        """
        if input_size < 1:
            raise ValueError("input_size must be positive.")
        operations = metrics["operations"] + metrics["function_calls"] + metrics["ast_nodes"]
        if metrics["nested_loops_depth"] > 0:
            operations *= input_size ** metrics["nested_loops_depth"]
        if metrics["recursive_functions"]:
            operations *= input_size

        runtime_seconds = operations / self.OPERATIONS_PER_SECOND
        return self.CPU_POWER_W * runtime_seconds / 3_600_000

    def calculate_carbon(
        self,
        energy_kwh: float,
        carbon_intensity_gco2e_per_kwh: float | None = None,
    ) -> float:
        """
        Calculate carbon emissions in gCO2e.

        Parameters
        ----------
        energy_kwh : float
            Energy consumption (kWh).
        carbon_intensity_gco2e_per_kwh : float or None, optional
            Carbon intensity of electricity (gCO2e/kWh). Uses
            ``CARBON_INTENSITY_GCO2E_PER_KWH`` if None.

        Returns
        -------
        float
            Carbon emission (gCO2e).

        Raises
        ------
        ValueError
            If the energy or the carbon intensity is negative.
        """
        if energy_kwh < 0:
            raise ValueError("Energy cannot be negative.")
        if carbon_intensity_gco2e_per_kwh is None:
            carbon_intensity_gco2e_per_kwh = self.CARBON_INTENSITY_GCO2E_PER_KWH
        if carbon_intensity_gco2e_per_kwh < 0:
            raise ValueError("Carbon intensity cannot be negative.")
        return energy_kwh * carbon_intensity_gco2e_per_kwh

    @staticmethod
    def _outest_loop(tree: ast.AST) -> list[ast.stmt]:
        """
        Find all the loops that are not nested in another loop.

        Parameters
        ----------
        tree : ast.AST
            AST of the code (or of a node).

        Returns
        -------
        list of ast.stmt
            Outermost ``for`` and ``while`` loops.
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
        Compute the loop nesting depth of a node.

        Parameters
        ----------
        node : ast.AST
            Node to analyse.

        Returns
        -------
        int
            Maximum number of nested loops under the node (the node
            included).
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
        Check whether a call is a recursive call.

        Parameters
        ----------
        call : ast.Call
            Call inside a function named ``function_name``.
        function_name : str
            Name of the function.

        Returns
        -------
        bool
            True if the call refers to the function named ``function_name``.
        """
        func = call.func

        if isinstance(func, ast.Name):
            return func.id == function_name
        return isinstance(func, ast.Attribute) and func.attr == function_name

    @log
    def detect_antipatterns(self, tree: ast.Module) -> list[AntiPattern]:
        """
        Detect all the antipatterns in a Python code.

        Parameters
        ----------
        tree : ast.Module
            AST (Abstract Syntax Tree) of the code.

        Returns
        -------
        list of AntiPattern
            Nested loops (depth >= 2) and recursive calls found in the code.
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
        Calculate the number of iterations of a loop.

        Parameters
        ----------
        node : ast.stmt
            ``for`` or ``while`` loop.

        Returns
        -------
        int
            Number of iterations of the loop, or ``DEFAULT_LOOP_LENGTH``
            if it cannot be known statically.
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
        Calculate the complexity of a loop, including its inner loops.

        Parameters
        ----------
        node : ast.stmt
            Loop to analyse.

        Returns
        -------
        int
            Complexity of the loop.
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
        Count the recursive calls made by one execution of a function.

        A call inside a loop is counted once per iteration.

        Parameters
        ----------
        node : ast.AST
            Function to analyse.
        function_name : str
            Name of the function.

        Returns
        -------
        int
            Number of recursive calls.
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
    def estimate_complexity(self, tree: ast.Module) -> float:
        """
        Estimate the complexity of a Python code.

        Parameters
        ----------
        tree : ast.Module
            AST of the code to estimate.

        Returns
        -------
        float
            Complexity of the code.
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
