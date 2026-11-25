import ast
from dataclasses import dataclass, field

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from business_object.file.codefile import CodeFile
from business_object.machinetype.machinetype import MachineType
from utils.log_utils import log


@dataclass
class AstAnalysis:
    """
    Result of a single analysis of Python source code.

    Attributes
    ----------
    metrics : dict
        Metrics extracted from the Abstract Syntax Tree (AST).
    antipatterns : list of AntiPattern
        Antipatterns detected in the source code.
    complexity : float
        Estimated computational complexity of the code.
    energy_kwh : float
        Estimated energy consumption, in kilowatt-hours (kWh).
    carbon_gco2e : float
        Estimated carbon emissions, in grams of CO2 equivalent (gCO2e).
    """

    metrics: dict
    antipatterns: list[AntiPattern] = field(default_factory=list)
    complexity: float = 0.0
    energy_kwh: float = 0.0
    carbon_gco2e: float = 0.0


class EcoService:
    """
    Service responsible for AST analysis, computational complexity
    estimation, energy consumption estimation and carbon emission
    estimation.

    Attributes
    ----------
    machine_type : MachineType
        Machine configuration used for energy and carbon estimations.
    LOOP_TYPES : tuple of type
        AST node types corresponding to loop statements (``for`` and ``while``).
    CONDITION_TYPES : tuple of type
        AST node types corresponding to conditional statements and expressions.
    OPERATION_TYPES : tuple of type
        AST node types considered as computational operations.
    DEFAULT_LOOP_LENGTH : int
        Default number of iterations assumed when the loop length is unknown.
    DEFAULT_RECURSION_DEPTH : int
        Default recursion depth used for complexity estimation.
    """

    def __init__(self, machine_type: MachineType = MachineType.REFERENCE):
        self.machine_type = machine_type

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

        runtime_seconds = operations / self.machine_type.operations_per_second
        return self.machine_type.cpu_power_w * runtime_seconds / 3_600_000

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
            Carbon intensity of electricity (gCO2e/kWh)

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
            carbon_intensity_gco2e_per_kwh = self.machine_type.carbon_intensity_gco2e_per_kwh
        if carbon_intensity_gco2e_per_kwh < 0:
            raise ValueError("Carbon intensity cannot be negative.")
        return energy_kwh * carbon_intensity_gco2e_per_kwh

    @log
    def _outest_loop(self, tree: ast.AST) -> list[ast.stmt]:
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
        loops = []

        for child in ast.iter_child_nodes(tree):
            if isinstance(child, self.LOOP_TYPES):
                loops.append(child)
            else:
                loops.extend(self._outest_loop(child))

        return loops

    @log
    def _loop_depth(self, node: ast.AST) -> int:
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
        depth = 0
        for child in ast.iter_child_nodes(node):
            child_depth = self._loop_depth(child)
            if child_depth > depth:
                depth = child_depth

        return depth + isinstance(node, self.LOOP_TYPES)

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
        for loop in self._outest_loop(tree):
            depth = self._loop_depth(loop)
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
                    if isinstance(node, ast.Call) and self._is_recursive_call(
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
    def _collect_variables(tree: ast.AST) -> dict:
        """
        Collect the variables assigned with a literal value.

        Only simple assignments such as ``n = 100`` or ``my_list = [1, 2, 3]``
        are kept. An assignment whose value is not a literal, such as
        ``n = int(input())``, is ignored.

        Parameters
        ----------
        tree : ast.AST
            The AST of the code.

        Returns
        -------
        dict
            The variables and their values, such as
            ``{"n": 100, "my_list": [1, 2, 3]}``.
        """
        variables = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                try:
                    variables[node.targets[0].id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):  # n = int(input()) : not a literal
                    pass

        return variables

    @staticmethod
    def _loop_length(node: ast.stmt, variables: dict | None = None) -> int:
        """
        Calculate the number of iterations of a loop.

        The length is found for a ``for`` loop over a list, a tuple, a set,
        a string, a variable whose value is known, or a ``range`` whose
        arguments are integers or known variables.

        Parameters
        ----------
        node : ast.stmt
            A ``for`` or ``while`` loop.
        variables : dict or None, default None
            The variables of the code, such as
            ``{"n": 100, "my_list": [1, 2, 3]}``.

        Returns
        -------
        int
            The number of iterations of the loop, or ``DEFAULT_LOOP_LENGTH``
            if it cannot be known (``while`` loop, unknown variable,
            ``range(n + 1)``...).
        """
        variables = variables or {}

        if isinstance(node, ast.For):
            iteration = node.iter

            # for i in [1, 2, 3] / (1, 2, 3) / {1, 2, 3}
            if isinstance(iteration, (ast.List, ast.Tuple, ast.Set)):
                return len(iteration.elts)

            # for i in "abc"
            if isinstance(iteration, ast.Constant) and isinstance(iteration.value, (str, bytes)):
                return len(iteration.value)

            # for i in my_list
            if isinstance(iteration, ast.Name):
                value = variables.get(iteration.id)
                if isinstance(value, (list, tuple, set, dict, str, bytes)):
                    return len(value)

            # for i in range(3) / range(n) / range(2, 10, 2)
            if (
                isinstance(iteration, ast.Call)
                and isinstance(iteration.func, ast.Name)
                and iteration.func.id == "range"
            ):
                if not 1 <= len(iteration.args) <= 3 or iteration.keywords:
                    return 0

                values = []
                for arg in iteration.args:
                    if isinstance(arg, ast.Constant):  # range(3)
                        values.append(arg.value)
                    elif isinstance(arg, ast.Name):  # range(n)
                        values.append(variables.get(arg.id))
                    else:  # range(n + 1), range(len(x))...
                        values.append(None)

                if None in values:
                    return EcoService.DEFAULT_LOOP_LENGTH

                try:
                    return len(range(*values))
                except (ValueError, TypeError):
                    return 0

        # Cannot know the length : while / unknown iterable
        return EcoService.DEFAULT_LOOP_LENGTH

    @staticmethod
    def _loop_complexity(node: ast.stmt, variables: dict | None = None) -> int:
        """
        Calculate the complexity of a loop.

        The complexity of a loop is its length. When other loops are nested in
        it, its length is multiplied by the sum of the complexities of the
        loops it directly contains.

        Parameters
        ----------
        node : ast.stmt
            A ``for`` or ``while`` loop.
        variables : dict or None, default None
            The variables of the code, such as
            ``{"n": 100, "my_list": [1, 2, 3]}``.

        Returns
        -------
        int
            The complexity of the loop.
        """
        complexity = EcoService._loop_length(node, variables)

        if EcoService()._loop_depth(node) >= 2:
            inner_complexity = 0
            for inner_loop in EcoService()._outest_loop(node):
                inner_complexity += EcoService._loop_complexity(inner_loop, variables)
            return complexity * inner_complexity

        return complexity

    def _count_recursive_calls(
        self, node: ast.AST, function_name: str, variables: dict | None = None
    ) -> int:
        """
        Count the recursive calls made by one execution of a function.

        A call inside a loop is counted once per iteration of the loop.

        Parameters
        ----------
        node : ast.AST
            The function to analyse, or one of its nodes.
        function_name : str
            The name of the function.
        variables : dict or None, default None
            The variables of the code, used to find the length of the loops,
            such as ``{"n": 100, "my_list": [1, 2, 3]}``.

        Returns
        -------
        int
            The number of recursive calls.
        """
        total = 0

        for child in ast.iter_child_nodes(node):
            count = EcoService()._count_recursive_calls(child, function_name, variables)

            if isinstance(child, ast.Call) and EcoService._is_recursive_call(child, function_name):
                count += 1

            if isinstance(child, self.LOOP_TYPES):
                count *= EcoService._loop_length(child, variables)

            total += count

        return total

    @log
    def estimate_complexity(self, tree: ast.Module) -> float:
        """
        Estimate the complexity of a Python code.

        The complexity is the sum of a base cost of 1, the complexity of all
        the loops, and the additional cost of the recursive functions.

        Parameters
        ----------
        tree : ast.Module
            The AST of the code to estimate.

        Returns
        -------
        float
            The estimated complexity of the code.
        """
        variables = self._collect_variables(tree)

        complexity = 1

        for loop in self._outest_loop(tree):
            complexity += self._loop_complexity(loop, variables)

        for function in ast.walk(tree):
            if not isinstance(function, ast.FunctionDef):
                continue

            calls = self._count_recursive_calls(function, function.name, variables)
            if calls == 0:
                continue

            executions = sum(
                calls**level for level in range(self.DEFAULT_RECURSION_DEPTH + 1)
            )

            one_execution = 1
            for loop in self._outest_loop(function):
                one_execution += self._loop_complexity(loop, variables)

            complexity += one_execution * (executions - 1)

        return float(complexity)
