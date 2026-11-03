import ast
from dataclasses import dataclass, field

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


class AstService:
    """Service responsible for parsing and analysing Python code."""

    @staticmethod
    def parse(code_file: CodeFile) -> ast.Module:
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
