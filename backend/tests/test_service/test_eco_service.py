import ast
from textwrap import dedent
from types import SimpleNamespace

import pytest

from business_object.machinetype.machinetype import MachineType
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
        pytest.param(
            """x = 1""",
            [],
            id="no_loop"),
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
    res = EcoService()._outest_loop(tree)

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
    res = EcoService()._loop_depth(node)

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
# _collect_variables
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("n = 100", {"n": 100}, id="integer"),
        pytest.param("my_list = [1, 2, 3]", {"my_list": [1, 2, 3]}, id="list"),
        # Valeur non littérale ou cible qui n'est pas un simple nom : ignorée
        pytest.param("n = int(input())", {}, id="not_a_literal"),
        pytest.param("x[0] = 5", {}, id="subscript_target"),
    ],
)
def test_collect_variables(source, expected):
    """Collect the variables assigned with a literal value"""

    # GIVEN
    tree = ast.parse(source)

    # WHEN
    res = EcoService._collect_variables(tree)

    # THEN
    assert res == expected


# =============================================================================
# _loop_length
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("for i in range(2, 10, 2):\n    pass", 4, id="range_start_stop_step"),
        pytest.param("for a in [1, 2, 3, 4]:\n    pass", 4, id="literal_list"),
        pytest.param("for c in 'abc':\n    pass", 3, id="literal_string"),
        # Range incohérent : 0 itération
        pytest.param("for i in range():\n    pass", 0, id="range_without_argument"),
        pytest.param("for i in range(0, 5, 0):\n    pass", 0, id="range_step_zero"),
        # Longueur inconnue (sans dictionnaire de variables) : valeur par défaut
        pytest.param("for a in x:\n    pass", DEFAULT_LENGTH, id="unknown_variable"),
        pytest.param("for i in range(n):\n    pass", DEFAULT_LENGTH, id="range_unknown_variable"),
        pytest.param("for i in range(len(x)):\n    pass", DEFAULT_LENGTH, id="range_len"),
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


@pytest.mark.parametrize(
    "source, variables, expected",
    [
        pytest.param("for i in range(n):\n    pass", {"n": 100}, 100, id="range_with_variable"),
        pytest.param(
            "for x in my_list:\n    pass", {"my_list": [1, 2, 3]}, 3, id="list_variable"
        ),
        pytest.param(
            "for x in n:\n    pass", {"n": 100}, DEFAULT_LENGTH, id="variable_not_a_collection"
        ),
    ],
)
def test_loop_length_with_variables(source, variables, expected):
    """Use the variables of the code to find the length of a loop"""

    # GIVEN
    loop = ast.parse(source).body[0]

    # WHEN
    res = EcoService._loop_length(loop, variables)

    # THEN
    assert res == expected


# =============================================================================
# _loop_complexity
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
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
        pytest.param(
            "def fib(n):\n    return fib(n - 1) + fib(n - 2)", 2, id="two_recursive_calls"
        ),
        pytest.param(
            "def f(n):\n    for i in range(2):\n        for j in range(3):\n"
            "            f(n - 1)",
            6,
            id="recursive_call_in_nested_loops",
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
    res = EcoService()._count_recursive_calls(function, function.name)

    # THEN
    assert res == expected


def test_count_recursive_calls_with_variables():
    """The length of the loop is found thanks to the variables"""

    # GIVEN
    function = ast.parse("def f(n):\n    for i in range(k):\n        f(n - 1)").body[0]

    # WHEN
    res = EcoService()._count_recursive_calls(function, function.name, {"k": 4})

    # THEN
    assert res == 4


# =============================================================================
# estimate_complexity
# =============================================================================


@pytest.mark.parametrize(
    "source, expected",
    [
        pytest.param("x = 1", 1, id="no_loop"),
        pytest.param(
            "for a in range(3):\n    pass\nfor b in range(4):\n    pass",
            1 + 3 + 4,
            id="sequential_loops",
        ),
        # Variables du code
        pytest.param(
            "n = 100\nfor i in range(n):\n    pass", 1 + 100, id="range_with_variable"
        ),
        pytest.param(
            "n = 4\nfor i in range(n):\n    for j in range(n):\n        pass",
            1 + 16,
            id="nested_loops_with_variable",
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
            "def f(n):\n    for a in range(5):\n        pass\n    return f(n - 1)",
            6 * (DEFAULT_DEPTH + 1),  # une exécution coûte 1 + 5, et il y en a 1 + profondeur
            id="loop_and_recursion",
        ),
        pytest.param(
            "def f(n):\n    for i in range(2):\n        f(n - 1)",
            3 * (2 ** (DEFAULT_DEPTH + 1) - 1),  # une exécution coûte 1 + 2, avec 2 appels
            id="recursive_call_in_a_loop",
        ),
    ],
)
def test_estimate_complexity(source, expected):
    """Estimate the complexity of a code according to its loops, variables and recursions"""

    # GIVEN
    tree = EcoService.parse(code_file(source))

    # WHEN
    res = EcoService().estimate_complexity(tree)

    # THEN
    assert res == expected


def test_estimate_complexity_returns_a_float():
    """The complexity is returned as a float"""

    # GIVEN
    tree = EcoService.parse(code_file("for i in range(3):\n    pass"))

    # WHEN
    res = EcoService().estimate_complexity(tree)

    # THEN
    assert isinstance(res, float)


def test_estimate_complexity_with_bytes_content():
    """Estimate the complexity of a code stored as bytes"""

    # GIVEN
    tree = EcoService.parse(code_file(b"for i in range(3):\n    pass"))

    # WHEN
    res = EcoService().estimate_complexity(tree)

    # THEN
    assert res == 1 + 3


def metrics(operations=0, function_calls=0, ast_nodes=0, depth=0, recursive=None):
    """Helper: fake metrics dictionary (keys read by calculate_energy)"""
    return {
        "operations": operations,
        "function_calls": function_calls,
        "ast_nodes": ast_nodes,
        "nested_loops_depth": depth,
        "recursive_functions": recursive or set(),
    }


def expected_energy(machine, operations):
    """Helper: expected energy (kWh) for a number of operations on a machine"""
    runtime_seconds = operations / machine.operations_per_second
    return machine.cpu_power_w * runtime_seconds / 3_600_000


# =============================================================================
# __init__
# =============================================================================


def test_init_default_machine():
    """The default machine is REFERENCE"""

    # GIVEN / WHEN
    service = EcoService()

    # THEN
    assert service.machine_type is MachineType.REFERENCE


@pytest.mark.parametrize("machine", list(MachineType), ids=lambda m: m.name.lower())
def test_init_with_machine(machine):
    """The machine given to the constructor is kept"""

    # GIVEN / WHEN
    service = EcoService(machine)

    # THEN
    assert service.machine_type is machine


# =============================================================================
# calculate_energy
# =============================================================================


@pytest.mark.parametrize(
    "source_metrics, input_size, expected_operations",
    [
        pytest.param(metrics(operations=2, function_calls=3, ast_nodes=5), 1000, 10, id="no_loop"),
        pytest.param(metrics(ast_nodes=10, depth=1), 1000, 10 * 1000, id="one_loop"),
        pytest.param(metrics(ast_nodes=10, depth=2), 1000, 10 * 1000**2, id="nested_loops"),
        pytest.param(
            metrics(ast_nodes=10, recursive={"f"}), 1000, 10 * 1000, id="recursion"
        ),
        pytest.param(
            metrics(ast_nodes=10, depth=1, recursive={"f"}),
            10,
            10 * 10 * 10,
            id="loop_and_recursion",
        ),
    ],
)
def test_calculate_energy(source_metrics, input_size, expected_operations):
    """Estimate the energy from the number of operations on the default machine"""

    # GIVEN
    service = EcoService()

    # WHEN
    res = service.calculate_energy(source_metrics, input_size)

    # THEN
    assert res == pytest.approx(expected_energy(MachineType.REFERENCE, expected_operations))


@pytest.mark.parametrize("machine", list(MachineType), ids=lambda m: m.name.lower())
def test_calculate_energy_uses_the_machine(machine):
    """The energy depends on the operations per second and CPU power of the machine"""

    # GIVEN
    service = EcoService(machine)
    source_metrics = metrics(ast_nodes=10, depth=1)

    # WHEN
    res = service.calculate_energy(source_metrics, 1000)

    # THEN
    assert res == pytest.approx(expected_energy(machine, 10 * 1000))


def test_calculate_energy_differs_between_machines():
    """Two machines with a different CPU give a different energy for the same code"""

    # GIVEN
    source_metrics = metrics(ast_nodes=10, depth=1)

    # WHEN
    reference = EcoService(MachineType.REFERENCE).calculate_energy(source_metrics)
    raspberry = EcoService(MachineType.RASPBERRY_PI).calculate_energy(source_metrics)

    # THEN
    assert reference != pytest.approx(raspberry)


@pytest.mark.parametrize("input_size", [0, -1], ids=["zero", "negative"])
def test_calculate_energy_invalid_input_size(input_size):
    """Fail to estimate the energy because input_size is lower than 1"""

    # GIVEN
    service = EcoService()

    # WHEN / THEN
    with pytest.raises(ValueError):
        service.calculate_energy(metrics(ast_nodes=10), input_size)


# =============================================================================
# calculate_carbon
# =============================================================================


@pytest.mark.parametrize("machine", list(MachineType), ids=lambda m: m.name.lower())
def test_calculate_carbon_uses_the_machine(machine):
    """Without explicit intensity, the carbon intensity of the machine is used"""

    # GIVEN
    service = EcoService(machine)

    # WHEN
    res = service.calculate_carbon(2.0)

    # THEN
    assert res == pytest.approx(2.0 * machine.carbon_intensity_gco2e_per_kwh)


def test_calculate_carbon_world_mix_vs_reference():
    """The world mix (450 gCO2e/kWh) emits 9 times more than the reference (50 gCO2e/kWh)"""

    # GIVEN
    energy = 1.0

    # WHEN
    reference = EcoService(MachineType.REFERENCE).calculate_carbon(energy)
    world_mix = EcoService(MachineType.REFERENCE_WORLD_MIX).calculate_carbon(energy)

    # THEN
    assert world_mix == pytest.approx(9 * reference)


def test_calculate_carbon_explicit_intensity_overrides_machine():
    """An explicit carbon intensity has priority over the one of the machine"""

    # GIVEN
    service = EcoService(MachineType.REFERENCE_WORLD_MIX)

    # WHEN
    res = service.calculate_carbon(2.0, 100.0)

    # THEN
    assert res == pytest.approx(200.0)


def test_calculate_carbon_zero_energy():
    """No energy means no carbon emission"""

    # GIVEN
    service = EcoService()

    # WHEN
    res = service.calculate_carbon(0.0)

    # THEN
    assert res == 0.0


@pytest.mark.parametrize(
    "energy, intensity",
    [
        pytest.param(-1.0, None, id="negative_energy"),
        pytest.param(1.0, -50.0, id="negative_intensity"),
    ],
)
def test_calculate_carbon_invalid_values(energy, intensity):
    """Fail to calculate the carbon emission because a value is negative"""

    # GIVEN
    service = EcoService()

    # WHEN / THEN
    with pytest.raises(ValueError):
        service.calculate_carbon(energy, intensity)


# =============================================================================
# analyze
# =============================================================================


def test_analyze_depends_on_the_machine():
    """The machine changes the energy and carbon, not the metrics nor the complexity"""

    # GIVEN
    source = code_file("for i in range(3):\n    x = i + 1")

    # WHEN
    reference = EcoService(MachineType.REFERENCE).analyze(source)
    raspberry = EcoService(MachineType.RASPBERRY_PI).analyze(source)

    # THEN
    assert reference.metrics == raspberry.metrics
    assert reference.complexity == raspberry.complexity
    assert reference.energy_kwh != pytest.approx(raspberry.energy_kwh)
    assert reference.carbon_gco2e != pytest.approx(raspberry.carbon_gco2e)


def test_analyze_energy_matches_calculate_energy():
    """The energy returned by analyze is the one computed from its own metrics"""

    # GIVEN
    service = EcoService(MachineType.LAPTOP)
    source = code_file("for i in range(3):\n    x = i + 1")

    # WHEN
    res = service.analyze(source)

    # THEN
    assert res.energy_kwh == pytest.approx(service.calculate_energy(res.metrics))
    assert res.carbon_gco2e == pytest.approx(service.calculate_carbon(res.energy_kwh))
