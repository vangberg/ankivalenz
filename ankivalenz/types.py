from dataclasses import dataclass, field
from typing import Tuple, Union


@dataclass
class Delimeter:
    contents: str


PathNode = Tuple[str, list["Node"]]
BasicNode = Tuple[str, Delimeter, str]
StandaloneNode = Tuple[Delimeter, str]
ClozeNode = str

Node = Union[list["Node"], PathNode, BasicNode, StandaloneNode, ClozeNode]


@dataclass(order=True)
class BasicCard:
    question: str
    answer: str
    path: list[str]
    reverse: bool = False


@dataclass(order=True)
class ClozeCard:
    question: str
    path: list[str]


Card = Union[BasicCard, ClozeCard]

Path = list[str]
