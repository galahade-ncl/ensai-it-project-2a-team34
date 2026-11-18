import ast
from textwrap import dedent

import pytest

from service.eco_service import EcoService
from business_object.file.codefile import CodeFile


DEFAULT_LENGTH = 10
DEFAULT_DEPTH = 10


def code_file(source):
    """Construit un vrai CodeFile, conformément à l'API du service."""
    content = dedent(source).strip() if isinstance(source, str) else source
    if isinstance(content, str):
        content = content.encode("utf-8")
    return CodeFile("test.py", content, ".py")


# ============================================================
# TESTS ENERGY
# ============================================================

@pytest.mark.parametrize(
    "source, input_size",
    [
        ("x = 1", 1),
        ("for i in range(3):\n    print(i)", 10),
        ("def fact(n):\n    return fact(n - 1)", 10),
        ("", 100),
    ],
)
def test_calculate_energy(source, input_size):
    result = EcoService().calculate_energy(code_file(source), input_size)
    assert result >= 0
    assert isinstance(result, float)


@pytest.mark.parametrize("input_size", [0, -1, -100])
def test_calculate_energy_invalid_input_size(input_size):
    with pytest.raises(ValueError):
        EcoService().calculate_energy(code_file("x = 1"), input_size)


# ============================================================
# TESTS CARBON
# ============================================================

def test_calculate_carbon_default_intensity():
    service = EcoService()
    source = code_file("x = 1")
    energy = service.calculate_energy(source)
    result = service.calculate_carbon(source)
    assert result == pytest.approx(
        energy * service.CARBON_INTENSITY_GCO2E_PER_KWH
    )


def test_calculate_carbon_custom_intensity():
    service = EcoService()
    source = code_file("x = 1")
    energy = service.calculate_energy(source)
    result = service.calculate_carbon(
        source, carbon_intensity_gco2e_per_kwh=400
    )
    assert result == pytest.approx(energy * 400)


def test_calculate_carbon_zero_energy():
    assert EcoService()._calculate_carbon(0, 0) == 0


@pytest.mark.parametrize("intensity", [-1, -100])
def test_calculate_carbon_negative_intensity(intensity):
    with pytest.raises(ValueError):
        EcoService().calculate_carbon(
            code_file("x = 1"),
            carbon_intensity_gco2e_per_kwh=intensity,
        )


def test_calculate_carbon_rejects_invalid_input_size():
    with pytest.raises(ValueError):
        EcoService().calculate_carbon(
            code_file("x = 1"), input_size=0
        )


# ============================================================
# TESTS OUTEST LOOP
# ============================================================

@pytest.mark.parametrize(
    "source, expected_lines",
    [
        ("x = 1", []),
        ("for a in x:\n    pass", [1]),
        ("for a in x:\n    for b in y:\n        pass", [1]),
        ("for a in x:\n    pass\nfor b in y:\n    pass", [1, 3]),
        ("def f(x):\n    for a in x:\n        pass", [2]),
        (
            "for a in x:\n    if a:\n        for b in y:\n            pass",
            [1],
        ),
        (
            "def f(x):\n    for a in x:\n        pass\n"
            "\ndef g(x):\n    while x:\n        pass",
            [2, 6],
        ),
        ("while x:\n    pass", [1]),
    ],
)
def test_outest_loop(source, expected_lines):
    tree = ast.parse(source)
    res = EcoService._outest_loop(tree)
    assert [loop.lineno for loop in res] == expected_lines


# ============================================================
# TESTS LOOP DEPTH
# ============================================================

@pytest.mark.parametrize(
    "source, expected_depth",
    [
        ("x = 1", 0),
        ("for a in x:\n    pass", 1),
        ("for a in x:\n    for b in y:\n        pass", 2),
        (
            "for a in x:\n    for b in y:\n"
            "        for c in z:\n            pass",
            3,
        ),
        ("for a in x:\n    while y:\n        pass", 2),
        (
            "for a in x:\n    for b in y:\n        pass\n"
            "    for c in z:\n        for d in w:\n            pass",
            3,
        ),
        (
            "for a in x:\n    if a:\n        for b in y:\n            pass",
            2,
        ),
        (
            "def f(x):\n    for a in x:\n        for b in a:\n            pass",
            2,
        ),
    ],
)
def test_loop_depth(source, expected_depth):
    node = ast.parse(source).body[0]
    res = EcoService._loop_depth(node)
    assert res == expected_depth


# ============================================================
# TESTS RECURSIVE CALL
# ============================================================

@pytest.mark.parametrize(
    "call_source, function_name, expected",
    [
        ("fact(n - 1)", "fact", True),
        ("print(n)", "fact", False),
        ("self.fact(n - 1)", "fact", True),
        ("cls.fact(n - 1)", "fact", True),
        ("other.fact(n)", "fact", True),
        ("a.b.fact(n)", "fact", True),
        ("other.save(n)", "fact", False),
        ("functions[0](n)", "fact", False),
        ("factory()(n)", "fact", False),
    ],
)
def test_is_recursive_call(call_source, function_name, expected):
    call = ast.parse(call_source).body[0].value
    res = EcoService._is_recursive_call(call, function_name)
    assert res is expected


# ============================================================
# TESTS ANTIPATTERNS
# ============================================================

def summarize(antipattern):
    """Résume un anti-pattern en (type, ligne, détail)."""
    kind = type(antipattern).__name__
    detail = (
        antipattern.depth
        if kind == "NestedLoop"
        else antipattern.function_name
    )
    return kind, antipattern.line, detail


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            "x = 1\nfor i in range(3):\n    print(i)",
            [],
        ),
        (
            "for a in x:\n    for b in y:\n        pass",
            [("NestedLoop", 1, 2)],
        ),
        (
            "for a in x:\n    for b in y:\n"
            "        for c in z:\n            pass",
            [("NestedLoop", 1, 3)],
        ),
        (
            "def f(x):\n    for a in x:\n"
            "        for b in a:\n            pass",
            [("NestedLoop", 2, 2)],
        ),
        (
            "for a in x:\n    pass\nfor b in y:\n    pass",
            [],
        ),
        (
            "for a in x:\n    for b in y:\n        pass\n"
            "    for c in z:\n        for d in w:\n"
            "            for e in v:\n                pass",
            [("NestedLoop", 1, 4)],
        ),
        (
            "def fact(n):\n"
            "    return 1 if n <= 1 else n * fact(n - 1)",
            [("RecursiveCall", 2, "fact")],
        ),
        (
            "class Tree:\n"
            "    def walk(self, node):\n"
            "        self.walk(node.left)",
            [("RecursiveCall", 3, "walk")],
        ),
        (
            "def f(n):\n    return g(n)\n"
            "\ndef g(n):\n    return n",
            [],
        ),
        (
            "def fact(n):\n    return n * fact(n - 1)\n"
            "\nfor a in x:\n    for b in y:\n        pass",
            [
                ("RecursiveCall", 2, "fact"),
                ("NestedLoop", 4, 2),
            ],
        ),
    ],
)
def test_detect_antipatterns(source, expected):
    tree = ast.parse(dedent(source).strip())
    res = EcoService().detect_antipatterns(code_file(source))
    assert sorted(summarize(a) for a in res) == sorted(expected)


# ============================================================
# TESTS LOOP LENGTH
# ============================================================

@pytest.mark.parametrize(
    "source, expected",
    [
        ("for i in range(3):\n    pass", 3),
        ("for i in range(2, 10, 2):\n    pass", 4),
        ("for i in range(5, 0, -1):\n    pass", 5),
        ("for i in range(-3, 3):\n    pass", 6),
        ("for i in range(0):\n    pass", 0),
        ("for a in [1, 2, 3, 4]:\n    pass", 4),
        ("for a in (1, 2):\n    pass", 2),
        ("for a in {1, 2, 3}:\n    pass", 3),
        ("for a in []:\n    pass", 0),
        ("for c in 'abc':\n    pass", 3),
        ("for c in b'ab':\n    pass", 2),
        ("for a in x:\n    pass", DEFAULT_LENGTH),
        ("for i in range(n):\n    pass", DEFAULT_LENGTH),
        ("for i in range(len(x)):\n    pass", DEFAULT_LENGTH),
        ("for i in range(0, 5, 0):\n    pass", DEFAULT_LENGTH),
        ("for i in range(1.5):\n    pass", DEFAULT_LENGTH),
        ("for a in 5:\n    pass", DEFAULT_LENGTH),
        ("for a in {1: 2}:\n    pass", DEFAULT_LENGTH),
        ("for a in enumerate(range(3)):\n    pass", DEFAULT_LENGTH),
        ("while x:\n    pass", DEFAULT_LENGTH),
    ],
)
def test_loop_length(source, expected):
    loop = ast.parse(source).body[0]
    res = EcoService._loop_length(loop)
    assert res == expected


# ============================================================
# TESTS LOOP COMPLEXITY
# ============================================================

@pytest.mark.parametrize(
    "source, expected",
    [
        ("for i in range(3):\n    pass", 3),
        (
            "for i in range(3):\n"
            "    for j in range(4):\n"
            "        for k in range(5):\n"
            "            pass",
            60,
        ),
        (
            "for a in range(2):\n"
            "    for b in range(3):\n"
            "        pass\n"
            "    for c in range(4):\n"
            "        pass",
            14,
        ),
        (
            "for a in range(2):\n"
            "    if a:\n"
            "        for b in range(3):\n"
            "            pass",
            6,
        ),
        (
            "for a in x:\n    for b in y:\n        pass",
            DEFAULT_LENGTH ** 2,
        ),
        (
            "for a in range(2):\n    while x:\n        pass",
            2 * DEFAULT_LENGTH,
        ),
        (
            "for a in range(3):\n"
            "    for b in range(0):\n        pass",
            0,
        ),
    ],
)
def test_loop_complexity(source, expected):
    loop = ast.parse(source).body[0]
    res = EcoService._loop_complexity(loop)
    assert res == expected


# ============================================================
# TESTS RECURSIVE CALL COUNT
# ============================================================

@pytest.mark.parametrize(
    "source, expected",
    [
        ("def f(n):\n    return g(n)", 0),
        ("def fact(n):\n    return n * fact(n - 1)", 1),
        (
            "def fib(n):\n"
            "    return fib(n - 1) + fib(n - 2)",
            2,
        ),
        ("def f(n):\n    if n:\n        f(n - 1)", 1),
        (
            "def f(n):\n"
            "    for i in range(2):\n"
            "        f(n - 1)",
            2,
        ),
        (
            "def f(n):\n"
            "    for i in range(2):\n"
            "        for j in range(3):\n"
            "            f(n - 1)",
            6,
        ),
        (
            "def f(n):\n    for a in x:\n        f(n - 1)",
            DEFAULT_LENGTH,
        ),
        (
            "def walk(self, node):\n"
            "    self.walk(node.left)\n"
            "    self.walk(node.right)",
            2,
        ),
    ],
)
def test_count_recursive_calls(source, expected):
    function = ast.parse(source).body[0]
    res = EcoService._count_recursive_calls(function, function.name)
    assert res == expected


# ============================================================
# TESTS ESTIMATE COMPLEXITY
# ============================================================

@pytest.mark.parametrize(
    "source, expected",
    [
        ("x = 1", 1),
        ("for i in range(3):\n    print(i)", 1 + 3),
        (
            "x = 0\n"
            "for i in range(3):\n"
            "    for j in range(4):\n"
            "        for k in range(5):\n"
            "            x += 1",
            1 + 60,
        ),
        (
            "for a in range(3):\n    pass\n"
            "for b in range(4):\n    pass",
            1 + 3 + 4,
        ),
        (
            "for a in range(2):\n"
            "    for b in range(3):\n"
            "        pass\n"
            "    for c in range(4):\n"
            "        pass",
            1 + 14,
        ),
        ("for a in x:\n    pass", 1 + DEFAULT_LENGTH),
        ("while x:\n    pass", 1 + DEFAULT_LENGTH),
        ("for a in range(0):\n    pass", 1),
        (
            "def f(x):\n    for a in range(5):\n        pass",
            1 + 5,
        ),
        (
            "def fact(n):\n    return n * fact(n - 1)",
            1,
        ),
        (
            "def fib(n):\n    return fib(n - 1) + fib(n - 2)",
            1,
        ),
        (
            "class Tree:\n"
            "    def walk(self, node):\n"
            "        self.walk(node.left)",
            1,
        ),
        (
            "def f(n):\n"
            "    for a in range(5):\n"
            "        pass\n"
            "    return f(n - 1)",
            66,
        ),
        (
            "def f(n):\n"
            "    for i in range(2):\n"
            "        f(n - 1)",
            6141,
        ),
        ("def f(n):\n    return g(n)", 1),
    ],
)
def test_estimate_complexity(source, expected):
    codefile = code_file(source)
    res = EcoService().estimate_complexity(codefile)
    assert res == expected


def test_estimate_complexity_returns_a_float():
    codefile = code_file("for i in range(3):\n    pass")
    res = EcoService().estimate_complexity(codefile)
    assert isinstance(res, float)


def test_estimate_complexity_with_bytes_content():
    codefile = code_file(b"for i in range(3):\n    pass")
    res = EcoService().estimate_complexity(codefile)
    assert res == 1 + 3
