import ast

import pytest

from service.eco_service import EcoService

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
