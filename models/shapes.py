from .abstract_shapes import Shape2d, Shape3d
from utils.constants import *


# 2D figure
class Rectangle(Shape2d):
    def __init__(self, width: float = 0, height: float = 0, area: float = 0):
        super().__init__()
        self.width = width
        self.height = height
        self.area = area
        self.available_operations += ["base", "height"]

    def calculate_area(self) -> float:
        return self.width * self.height

    def calculate_perimeter(self) -> float:
        if self.width == self.height:
            return 4 * self.height
        return 2 * (self.width + self.height)

    def calculate_base(self) -> float:
        return self.area / self.height

    def calculate_height(self) -> float:
        return self.area / self.width


class Circle(Shape2d):

    def __init__(self, radius: float = 0, diameter: float = 0, area: float = 0):
        super().__init__()
        self.radius = radius
        self.diameter = diameter
        self.area = area
        self.available_operations += ["diameter"]

    def calculate_area(self) -> float:
        return PI * self.radius**2

    def calculate_perimeter(self):
        return 2 * PI * self.radius

    def calculate_diameter(self):
        return self.diameter * 2


class Triangle(Shape2d):
    def __init__(self, a=0, b=0, c=0, base=0, height=0, angle1=0, angle2=0):
        super().__init__()
        self.a, self.b, self.c = a, b, c
        self.base, self.height = base, height
        self.angle1, self.angle2 = angle1, angle2
        self.available_operations += ["base", "height", "last_angle"]

    def calculate_area(self) -> float:
        return self.base * self.height / 2

    def calculate_perimeter(self) -> float:
        return self.a + self.b + self.c

    def calculate_base(self) -> float:
        return 2 * self.calculate_area() / self.base

    def calculate_height(self) -> float:
        return 2 * self.calculate_area() / self.height

    def calculate_last_angle(self):
        return 180 - (self.angle1 + self.angle2)


class RigthRectangle(Shape2d):
    def __init__(self, adjacent=0, opposite=0, hipotenuse=0, angle=0):
        super().__init__()
        self.adjacent = adjacent
        self.opposite = opposite
        self.hipotenuse = hipotenuse
        self.angle = angle
        self.available_operations += ["hipotenuse", "last_leg", "last_angle"]

    def calculate_area(self) -> float:
        return self.adjacent * self.opposite * 1 / 2

    def calculate_perimeter(self) -> float:
        return self.adjacent + self.opposite + self.hipotenuse

    def calculate_hipotenuse(self) -> float:
        return (self.adjacent**2 + self.opposite**2) ** (1 / 2)

    def calculate_last_leg(self) -> float:
        return self.hipotenuse**2 - (
            self.adjacent if self.adjacent == 0 else self.opposite
        )

    def calculate_last_angle(self) -> float:
        return 180 - (RECT_ANGLE + self.angle)


class Pentagon(Shape2d):
    def __init__(self, side=0):
        super().__init__()
        self.side = side

    def calculate_area(self) -> float:
        return (5 / 4) * self.side**2 / TAN_PI_5

    def calculate_perimeter(self) -> float:
        return 5 * self.side


# 3D figures
class Sphere(Shape3d):
    def __init__(self, radius: float = 0) -> None:
        super().__init__()
        self.radius = radius

    def calculate_surface_area(self) -> float:
        return 4 * PI * self.radius**2

    def calculate_volume(self) -> float:
        return 4 / 3 * PI * self.radius**3


class Parallelepiped(Shape3d):
    def __init__(self, lenght: float = 0, width: float = 0, height: float = 0) -> None:
        super().__init__()
        self.lenght = lenght
        self.width = width
        self.height = height

    def calculate_surface_area(self) -> float:
        return 2 * (
            self.lenght * self.width
            + self.lenght * self.height
            + self.height * self.width
        )

    def calculate_volume(self) -> float:
        return self.lenght * self.width * self.height


class Cylinder(Shape3d):
    def __init__(self, radius: float = 0, height: float = 0) -> None:
        super().__init__()
        self.radius = radius
        self.height = height

    def calculate_surface_area(self) -> float:
        return 2 * PI * self.radius * (self.radius + self.height)

    def calculate_volume(self) -> float:
        return PI * self.radius**2 * self.height


class Cone(Shape3d):
    def __init__(self, radius=0, height=0):
        super().__init__()
        self.radius, self.height = radius, height

    def calculate_volume(self) -> float:
        return (1 / 3) * PI * self.radius**2 * self.height

    def calculate_surface_area(self) -> float:
        l = (self.radius**2 + self.height**2) ** (1 / 2)
        return PI * self.radius * (self.radius + l)
