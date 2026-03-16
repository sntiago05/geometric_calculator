from abc import ABC, abstractmethod


from abc import ABC, abstractmethod


class Shape2d(ABC):
    def __init__(self) -> None:
        self.available_operations = ["area", "perimeter"]

    @abstractmethod
    def calculate_area(self) -> float:
        pass

    @abstractmethod
    def calculate_perimeter(self) -> float:
        pass


class Shape3d(ABC):

    def __init__(self) -> None:
        self.available_operations = ["volume", "surface_area"]

    @abstractmethod
    def calculate_volume(self) -> float:
        pass

    @abstractmethod
    def calculate_surface_area(self) -> float:
        pass
