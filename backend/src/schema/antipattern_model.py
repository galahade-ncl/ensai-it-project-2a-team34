from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag


def _class_name(value: Any) -> str:
    """Discriminator: the class name of the business object."""
    return type(value).__name__


# ---------------------
# Anti-patterns
# ---------------------
class AntiPatternBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_antipattern: int | None = None
    line: int
    description: str


class NestedLoopModel(AntiPatternBase):
    type: Literal["NestedLoop"] = "NestedLoop"
    depth: int


class RecursiveCallModel(AntiPatternBase):
    type: Literal["RecursiveCall"] = "RecursiveCall"
    function_name: str


AntiPatternModel = Annotated[
    Annotated[NestedLoopModel, Tag("NestedLoop")]
    | Annotated[RecursiveCallModel, Tag("RecursiveCall")],
    Discriminator(_class_name),
]
