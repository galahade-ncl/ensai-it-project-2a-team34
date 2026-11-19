from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag


def _class_name(value: Any) -> str:
    """
    Discriminator returning the class name of the business object.

    Parameters
    ----------
    value : Any
        Business object to serialize.

    Returns
    -------
    str
        Name of the class of ``value``.
    """
    return type(value).__name__


# ---------------------
# Anti-patterns
# ---------------------
class AntiPatternBase(BaseModel):
    """
    Base Pydantic model of an antipattern.

    Attributes
    ----------
    id_antipattern : int or None
        Unique identifier of the antipattern.
    line : int
        Line number where the antipattern was detected.
    description : str
        Description of the antipattern.
    """
    model_config = ConfigDict(from_attributes=True)

    id_antipattern: int | None = None
    line: int
    description: str


class NestedLoopModel(AntiPatternBase):
    """
    Pydantic model of a nested loop antipattern.

    Attributes
    ----------
    type : {'NestedLoop'}
        Type of the antipattern.
    depth : int
        Nesting depth of the loop.
    """
    type: Literal["NestedLoop"] = "NestedLoop"
    depth: int


class RecursiveCallModel(AntiPatternBase):
    """
    Pydantic model of a recursive call antipattern.

    Attributes
    ----------
    type : {'RecursiveCall'}
        Type of the antipattern.
    function_name : str
        Name of the function that calls itself.
    """
    type: Literal["RecursiveCall"] = "RecursiveCall"
    function_name: str


AntiPatternModel = Annotated[
    Annotated[NestedLoopModel, Tag("NestedLoop")]
    | Annotated[RecursiveCallModel, Tag("RecursiveCall")],
    Discriminator(_class_name),
]
