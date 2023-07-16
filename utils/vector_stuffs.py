import math

from numba import jit
from pygame import Vector2


def int_ify(vector: Vector2) -> (int, int):
    return int(vector.x), int(vector.y)


def int_ify_list(vector_list: list[Vector2]) -> list[tuple[int, int]]:
    return [int_ify(vector) for vector in vector_list]


# using numba to speed up the function
@jit(nopython=True, cache=True, fastmath=True)
def within_polygon(x: int, y: int, poly: list[[int, int]], tolerance=5):
    n = len(poly)
    inside = False
    x_ints = 0.0

    # Original polygon check
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_ints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_ints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    # Check distance to edges
    if not inside:
        for i in range(n):
            p1x, p1y = poly[i]
            p2x, p2y = poly[(i + 1) % n]
            h = math.hypot(p2y - p1y, p2x - p1x)
            dist = abs((p2y - p1y) * x - (p2x - p1x) * y + p2x * p1y - p2y * p1x) / h

            if dist <= tolerance:
                return True

    return inside