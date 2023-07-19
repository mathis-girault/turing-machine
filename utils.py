from enum import Enum
import functools
from typing import Literal, Callable
CombiVal = Literal[1, 2, 3, 4, 5]
Optionval = Literal[1, 2, 3, 4]

class Shape(Enum):
    """ Define a shape """
    TRIANGLE = "triangle"
    CARRE = "carre"
    ROND = "rond"

    @classmethod
    def list_shapes(cls) -> list:
        role_names = [member for _, member in cls.__members__.items()]
        return role_names

    @classmethod
    def print_list(cls) -> str:
        return f"Ordered shapes: ({', '.join([elem.value for elem in cls.list_shapes()])})"

class Verifs(Enum):
    """ Define game verificators """
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    
@functools.total_ordering
class Combi:
    """ Define in-game combination """
    triangle: CombiVal
    carre: CombiVal
    rond: CombiVal

    def __init__(self, triangle: CombiVal, carre: CombiVal, rond: CombiVal) -> None:
        assert carre in [1, 2, 3, 4, 5]
        assert rond in [1, 2, 3, 4, 5]
        assert triangle in [1, 2, 3, 4, 5]
        self.triangle = triangle
        self.carre = carre
        self.rond = rond

    def verify(self, function: Callable) -> bool:
        return function(self)

    def get_shape(self, shape: Shape) -> CombiVal:
        if shape == Shape.CARRE:
            return self.carre
        elif shape == Shape.ROND:
            return self.rond
        elif shape == Shape.TRIANGLE:
            return self.triangle
        raise ValueError(f"Shape {shape} is not valid")

    def count(self, value: CombiVal) -> int:
        return sum(1 for v in [self.carre, self.rond, self.triangle] if v == value)

    def __str__(self) -> str:
        return f"(▲ {self.triangle}, ■ {self.carre}, ● {self.rond})"

    def __gt__(self, other):
        assert isinstance(other, Combi)
        if self.triangle > other.triangle:
            return True
        if self.triangle < other.triangle:
            return False
        if self.carre > other.carre:
            return True
        if self.carre < other.carre:
            return False
        if self.rond > other.rond:
            return True
        return False

    def __eq__(self, other):
        assert isinstance(other, Combi)
        return self.carre == other.carre and self.rond == other.rond and self.triangle == other.triangle

    def __hash__(self):
        return hash((self.carre, self.rond, self.triangle))

    def __iter__(self):
        for shape in Shape.list_shapes():
            yield {shape: self.get_shape(shape)}
