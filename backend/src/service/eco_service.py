import ast

from business_object.antipattern.antipattern import Antipattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall

from utils.log_utils import log


class EcoService:
    """
    Service that handles business logic related to the eco analyse of a Python code
    """

    def outest_loop (tree: ast.AST) -> list[ast.stmt]:
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
                loops.extend(outest_loop(child))

        return loops

    def loop_depth(node: ast.AST) -> int:
        """
        Depth of a node
        Args:
            node (ast.AST) : The node
        Returns:
            An intege that is the depth of the node
        """
        depth = 0
        for child in ast.iter_child_nodes(node):

    @log
    def detect_antipatterns(self, tree: ast.Module) -> list[Antipattern]:
        """
        Detect all the antipatterns in a Python code
        Args:
            tree (ast.Module) : The AST (Abstract Synthax Tree) of the code
        Returns:
            A list of the Antipatterns of the code
        """
