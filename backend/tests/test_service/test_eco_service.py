import ast

from business_object.antipattern.antipattern import AntiPattern
from business_object.antipattern.nestedloop import NestedLoop
from business_object.antipattern.recursivecall import RecursiveCall
from service.eco_service import EcoService


@pytest.mark.parametrize(
    "tree, result",
    [
        (
            """
            x = 0
            for i in range(3):
                for j in range(4):
                    for k in range(5):
                        x +=1
            """,
            [NestedLoop(
                line=2,
                description="",
                depth=3,
                id_antipattern = None

            )])
        ]
    )