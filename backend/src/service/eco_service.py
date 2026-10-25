import ast

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from utils.log_utils import log


class EcoService:
    """
    Service that handles business logic related to the eco analyse of a Python code
    """

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
        return (
            isinstance(func, ast.Attribute) and
            func.attr == function_name
        )


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
                        id_antipattern = None
                    )

                )

        # Recursive call
        for func in ast.walk(tree):
            if  isinstance (func, ast.FunctionDef):
                for node in ast.walk(func):
                    if isinstance(node, ast.Call) and EcoService._is_recursive_call(node, func.name):
                        antipatterns.append(
                            RecursiveCall(
                                line=node.lineno,
                                description="Recursive_call",
                                function_name=func.name,
                                id_antipattern = None

                            )
                        )
        return antipatterns
