import ast
from textwrap import dedent
from types import SimpleNamespace

import pytest

from service.eco_service import EcoService

DEFAULT_LENGTH = 10
DEFAULT_DEPTH = 10

def code_file(source):
    """Utilitaire : faux CodeFile (seul l'attribut content est lu par EcoService)"""
    content = dedent(source).strip() if isinstance(source, str) else source
    return SimpleNamespace(content=content)


# =============================================================================
# _outest_loop
# =============================================================================


@pytest.mark.parametrize(
    "source, expected_lines",
    [
        pytest.param("x = 1", [], id="no_loop"),
        pytest.param("for a in x:\n    pass", [1], id="one_loop"),
        pytest.param(
            "for a in x:\n    for b in y:\n        pass",
            [1],
            id="nested_loops_keep_only_the_outer_one",
        ),
        pytest.param(
            "for a in x:\n    pass\nfor b in y:\n    pass",
            [1, 3],
            id="sequential_loops",
        ),
        pytest.param(
            "def f(x):\n    for a in x:\n        pass",
            [2],
            id="loop_inside_a_function",
        ),
        pytest.param(
            "for a in x:\n    if a:\n        for b in y:\n            pass",
            [1],
            id="loop_hidden_in_an_if_inside_a_loop",
        ),
        pytest.param(
            "def f(x):\n    for a in x:\n        pass\n\ndef g(x):\n    while x:\n        pass",
            [2, 6],
            id="loops_in_two_functions",
        ),
        pytest.param("while x:\n    pass", [1], id="while_loop"),
    ],
)
def test_outest_loop(source, expected_lines):
    """Find the loops that are not nested in another loop"""

    # GIVEN
    tree = ast.parse(source)

    # WHEN
    res = EcoService._outest_loop(tree)

    # THEN
    assert [loop.lineno for loop in res] == expected_lines


# =============================================================================
# _loop_depth
# =============================================================================


@pytest.mark.parametrize(
    "source, expected_depth",
    [
        pytest.param("x = 1", 0, id="not_a_loop"),
        pytest.param("for a in x:\n    pass", 1, id="single_loop"),
        pytest.param(
            "for a in x:\n    for b in y:\n        pass",
            2,
            id="two_nested_loops",
        ),
        pytest.param(
            "for a in x:\n    for b in y:\n        for c in z:\n            pass",
            3,
            id="three_nested_loops",
        ),
        pytest.param(
            "for a in x:\n    while y:\n        pass",
            2,
            id="while_inside_for",
        ),
        pytest.param(
            "for a in x:\n    for b in y:\n        pass\n"
            "    for c in z:\n        for d in w:\n            pass",
            3,
            id="deepest_branch_wins",
        ),
        pytest.param(
            "for a in x:\n    if a:\n        for b in y:\n            pass",
            2,
            id="loop_hidden_in_an_if",
        ),
        pytest.param(
            "def f(x):\n    for a in x:\n        for b in a:\n            pass",
            2,
            id="function_is_not_counted",
        ),
    ],
)
def test_loop_depth(source, expected_depth):
    """Calculate the maximum number of nested loops under a node"""

    # GIVEN
    node = ast.parse(source).body[0]

    # WHEN
    res = EcoService._loop_depth(node)

    # THEN
    assert res == expected_depth


# =============================================================================
# _is_recursive_call
# =============================================================================


@pytest.mark.parametrize(
    "call_source, function_name, expected",
    [
        pytest.param("fact(n - 1)", "fact", True, id="call_by_name"),
        pytest.param("print(n)", "fact", False, id="call_to_another_function"),
        pytest.param("self.fact(n - 1)", "fact", True, id="call_on_self"),
        pytest.param("cls.fact(n - 1)", "fact", True, id="call_on_cls"),
        pytest.param("other.fact(n)", "fact", True, id="same_method_name_on_another_object"),
        pytest.param("a.b.fact(n)", "fact", True, id="chained_attributes"),
        pytest.param("other.save(n)", "fact", False, id="another_method_name"),
        pytest.param("functions[0](n)", "fact", False, id="call_through_a_subscript"),
        pytest.param("factory()(n)", "fact", False, id="call_of_a_returned_value"),
    ],
)
def test_is_recursive_call(call_source, function_name, expected):
    """Verify if a call refers to the function named function_name"""

    # GIVEN
    call = ast.parse(call_source).body[0].value

    # WHEN
    res = EcoService._is_recursive_call(call, function_name)

    # THEN
    assert res is expected


def summarize(antipattern) -> tuple:
    """Résume un anti-pattern en (type, ligne, détail) pour le comparer facilement"""
    kind = type(antipattern).__name__
    detail = antipattern.depth if kind == "NestedLoop" else antipattern.function_name
    return (kind, antipattern.line, detail)


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param(
            """
            x = 1
            for i in range(3):
                print(i)
            """,
            [],
            id="no_antipattern",
        ),
        pytest.param(
            """
            for a in x:
                for b in y:
                    pass
            """,
            [("NestedLoop", 1, 2)],
            id="two_nested_loops",
        ),
        pytest.param(
            """
            for a in x:
                for b in y:
                    for c in z:
                        pass
            """,
            [("NestedLoop", 1, 3)],
            id="three_nested_loops",
        ),
        pytest.param(
            """
            def f(x):
                for a in x:
                    for b in a:
                        pass
            """,
            [("NestedLoop", 2, 2)],
            id="nested_loops_inside_a_function",
        ),
        pytest.param(
            """
            for a in x:
                pass
            for b in y:
                pass
            """,
            [],
            id="sequential_loops_are_not_nested",
        ),
        pytest.param(
            """
            for a in x:
                for b in y:
                    pass
                for c in z:
                    for d in w:
                        for e in v:
                            pass
            """,
            [("NestedLoop", 1, 4)],
            id="depth_is_the_deepest_branch",
        ),
        pytest.param(
            """
            def fact(n):
                return 1 if n <= 1 else n * fact(n - 1)
            """,
            [("RecursiveCall", 2, "fact")],
            id="recursive_function",
        ),
        pytest.param(
            """
            class Tree:
                def walk(self, node):
                    self.walk(node.left)
            """,
            [("RecursiveCall", 3, "walk")],
            id="recursive_method",
        ),
        pytest.param(
            """
            def f(n):
                return g(n)

            def g(n):
                return n
            """,
            [],
            id="call_to_another_function",
        ),
        pytest.param(
            """
            def fact(n):
                return n * fact(n - 1)

            for a in x:
                for b in y:
                    pass
            """,
            [("RecursiveCall", 2, "fact"), ("NestedLoop", 4, 2)],
            id="nested_loop_and_recursion",
        ),
    ],
)
def test_detect_antipatterns(source, expected):
    """Detect the antipatterns (type, line, depth or function name) of a Python code"""

    # GIVEN
    tree = ast.parse(dedent(source).strip())

    # WHEN
    res = EcoService().detect_antipatterns(tree)

    # THEN
    assert sorted(summarize(a) for a in res) == sorted(expected)


# =============================================================================
# _loop_length
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        # Longueur lue dans le code
        pytest.param("for i in range(3):\n    pass", 3, id="range_stop"),
        pytest.param("for i in range(2, 10, 2):\n    pass", 4, id="range_start_stop_step"),
        pytest.param("for i in range(5, 0, -1):\n    pass", 5, id="range_negative_step"),
        pytest.param("for i in range(-3, 3):\n    pass", 6, id="range_negative_start"),
        pytest.param("for i in range(0):\n    pass", 0, id="range_empty"),
        pytest.param("for a in [1, 2, 3, 4]:\n    pass", 4, id="literal_list"),
        pytest.param("for a in (1, 2):\n    pass", 2, id="literal_tuple"),
        pytest.param("for a in {1, 2, 3}:\n    pass", 3, id="literal_set"),
        pytest.param("for a in []:\n    pass", 0, id="empty_list"),
        pytest.param("for c in 'abc':\n    pass", 3, id="literal_string"),
        pytest.param("for c in b'ab':\n    pass", 2, id="literal_bytes"),
        # Longueur inconnue : valeur par défaut
        pytest.param("for a in x:\n    pass", DEFAULT_LENGTH, id="variable"),
        pytest.param("for i in range(n):\n    pass", DEFAULT_LENGTH, id="range_with_variable"),
        pytest.param("for i in range(len(x)):\n    pass", DEFAULT_LENGTH, id="range_len"),
        pytest.param("for i in range(0, 5, 0):\n    pass", DEFAULT_LENGTH, id="range_step_zero"),
        pytest.param("for i in range(1.5):\n    pass", DEFAULT_LENGTH, id="range_with_float"),
        pytest.param("for a in 5:\n    pass", DEFAULT_LENGTH, id="constant_not_iterable"),
        pytest.param("for a in {1: 2}:\n    pass", DEFAULT_LENGTH, id="literal_dict"),
        pytest.param(
            "for a in enumerate(range(3)):\n    pass", DEFAULT_LENGTH, id="enumerate"
        ),
        pytest.param("while x:\n    pass", DEFAULT_LENGTH, id="while_loop"),
    ],
)
def test_loop_length(source, expected):
    """Estimate the number of iterations of a loop"""

    # GIVEN
    loop = ast.parse(source).body[0]

    # WHEN
    res = EcoService._loop_length(loop)

    # THEN
    assert res == expected


# =============================================================================
# _loop_complexity
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("for i in range(3):\n    pass", 3, id="single_loop"),
        pytest.param(
            "for i in range(3):\n    for j in range(4):\n        for k in range(5):\n"
            "            pass",
            60,
            id="nested_loops_are_multiplied",
        ),
        pytest.param(
            "for a in range(2):\n    for b in range(3):\n        pass\n"
            "    for c in range(4):\n        pass",
            14,
            id="inner_loops_in_sequence_are_added",
        ),
        pytest.param(
            "for a in range(2):\n    if a:\n        for b in range(3):\n            pass",
            6,
            id="inner_loop_hidden_in_an_if",
        ),
        pytest.param(
            "for a in x:\n    for b in y:\n        pass",
            DEFAULT_LENGTH**2,
            id="unknown_lengths_use_the_default",
        ),
        pytest.param(
            "for a in range(2):\n    while x:\n        pass",
            2 * DEFAULT_LENGTH,
            id="while_inside_for",
        ),
        pytest.param(
            "for a in range(3):\n    for b in range(0):\n        pass",
            0,
            id="inner_loop_that_never_runs",
        ),
    ],
)
def test_loop_complexity(source, expected):
    """Calculate the complexity of a loop (nested loops are multiplied)"""

    # GIVEN
    loop = ast.parse(source).body[0]

    # WHEN
    res = EcoService._loop_complexity(loop)

    # THEN
    assert res == expected


# =============================================================================
# _count_recursive_calls
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("def f(n):\n    return g(n)", 0, id="not_recursive"),
        pytest.param("def fact(n):\n    return n * fact(n - 1)", 1, id="one_recursive_call"),
        pytest.param(
            "def fib(n):\n    return fib(n - 1) + fib(n - 2)", 2, id="two_recursive_calls"
        ),
        pytest.param(
            "def f(n):\n    if n:\n        f(n - 1)", 1, id="recursive_call_in_an_if"
        ),
        pytest.param(
            "def f(n):\n    for i in range(2):\n        f(n - 1)",
            2,
            id="recursive_call_in_a_loop_counts_once_per_iteration",
        ),
        pytest.param(
            "def f(n):\n    for i in range(2):\n        for j in range(3):\n"
            "            f(n - 1)",
            6,
            id="recursive_call_in_nested_loops",
        ),
        pytest.param(
            "def f(n):\n    for a in x:\n        f(n - 1)",
            DEFAULT_LENGTH,
            id="recursive_call_in_a_loop_of_unknown_length",
        ),
        pytest.param(
            "def walk(self, node):\n    self.walk(node.left)\n    self.walk(node.right)",
            2,
            id="recursive_method",
        ),
    ],
)
def test_count_recursive_calls(source, expected):
    """Count the recursive calls made by one execution of a function"""

    # GIVEN
    function = ast.parse(source).body[0]

    # WHEN
    res = EcoService._count_recursive_calls(function, function.name)

    # THEN
    assert res == expected


# =============================================================================
# estimate_complexity
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("x = 1", 1, id="no_loop"),
        pytest.param("for i in range(3):\n    print(i)", 1 + 3, id="one_loop"),
        pytest.param(
            "x = 0\nfor i in range(3):\n    for j in range(4):\n        for k in range(5):\n"
            "            x += 1",
            1 + 60,
            id="three_nested_loops",
        ),
        pytest.param(
            "for a in range(3):\n    pass\nfor b in range(4):\n    pass",
            1 + 3 + 4,
            id="sequential_loops",
        ),
        pytest.param(
            "for a in range(2):\n    for b in range(3):\n        pass\n"
            "    for c in range(4):\n        pass",
            1 + 14,
            id="nested_loop_with_two_inner_loops",
        ),
        pytest.param("for a in x:\n    pass", 1 + DEFAULT_LENGTH, id="loop_of_unknown_length"),
        pytest.param("while x:\n    pass", 1 + DEFAULT_LENGTH, id="while_loop"),
        pytest.param(
            "for a in range(0):\n    pass", 1, id="loop_that_never_runs"
        ),
        pytest.param(
            "def f(x):\n    for a in range(5):\n        pass",
            1 + 5,
            id="loop_inside_a_function",
        ),
        # Récursion : (1 + profondeur) exécutions pour un appel, arbre binaire pour deux appels
        pytest.param(
            "def fact(n):\n    return n * fact(n - 1)",
            DEFAULT_DEPTH + 1,
            id="linear_recursion",
        ),
        pytest.param(
            "def fib(n):\n    return fib(n - 1) + fib(n - 2)",
            2 ** (DEFAULT_DEPTH + 1) - 1,
            id="double_recursion",
        ),
        pytest.param(
            "class Tree:\n    def walk(self, node):\n        self.walk(node.left)",
            DEFAULT_DEPTH + 1,
            id="recursive_method",
        ),
        pytest.param(
            "def f(n):\n    for a in range(5):\n        pass\n    return f(n - 1)",
            6 * (DEFAULT_DEPTH + 1),  # une exécution coûte 1 + 5, et il y en a 1 + profondeur
            id="loop_and_recursion",
        ),
        pytest.param(
            "def f(n):\n    for i in range(2):\n        f(n - 1)",
            3 * (2 ** (DEFAULT_DEPTH + 1) - 1),  # une exécution coûte 1 + 2, avec 2 appels
            id="recursive_call_in_a_loop",
        ),
        pytest.param(
            "def f(n):\n    return g(n)", 1, id="call_to_another_function_is_not_recursion"
        ),
    ],
)
def test_estimate_complexity(source, expected):
    """Estimate the complexity of a code according to its loops and its recursions"""

    # GIVEN
    codefile = code_file(source)

    # WHEN
    res = EcoService().estimate_complexity(codefile)

    # THEN
    assert res == expected


def test_estimate_complexity_returns_a_float():
    """The complexity is returned as a float"""

    # GIVEN
    codefile = code_file("for i in range(3):\n    pass")

    # WHEN
    res = EcoService().estimate_complexity(codefile)

    # THEN
    assert isinstance(res, float)


def test_estimate_complexity_with_bytes_content():
    """Estimate the complexity of a code stored as bytes"""

    # GIVEN
    codefile = code_file(b"for i in range(3):\n    pass")

    # WHEN
    res = EcoService().estimate_complexity(codefile)

    # THEN
    assert res == 1 + 3
