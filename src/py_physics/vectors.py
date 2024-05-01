from copy import deepcopy
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def clone(self):
        return deepcopy(self)

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


def scale_vec(vec: Vec2, factor: float) -> Vec2:
    return Vec2(vec.x * factor, vec.y * factor)


def add_vectors(a: Vec2, b: Vec2, s: float = 1) -> Vec2:
    return Vec2(a.x + b.x * s, a.y + b.y * s)


def subtract_vectors(a: Vec2, b: Vec2, s: float = 1) -> Vec2:
    return Vec2(a.x - b.x * s, a.y - b.y * s)


def dot_product(a: Vec2, b: Vec2) -> float:
    return a.x * b.x + a.y * b.y
