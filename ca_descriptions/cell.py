
from dataclasses import dataclass
from enum import Enum


class State(Enum):
    NORMAL = 0
    BURNING = 1
    DEAD = 2

    def __str__(self) -> str:
        return self.name


class Type(Enum):
    CHAPARRAL = 0
    CANYON = 1
    FOREST = 2
    LAKE = 3
    TOWN = 4

    def __str__(self) -> str:
        return self.name

    def get_fuel(self):
        FUEL = {
            self.CANYON: 1,
            self.CHAPARRAL: 28,
            self.FOREST: 120,
        }
        return FUEL[self]


@dataclass
class Cell(object):
    def __init__(self, type: Type) -> None:
        self.type = type
        self.fuel = self.type.get_fuel()
        self.state = State.NORMAL

    def __str__(self):
        return f"""CELL
        Type: {self.type} 
        State: {self.state}
        Fuel: {self.fuel}  
        """

    def update(self, ignite: bool = False):

        # cell is dead if ran out of fuel
        if self.fuel == 0:
            self.state = State.DEAD

        # ignite the cell
        if ignite and self.state == State.NORMAL:
            self.state = State.BURNING

        # decrease fuel when burning
        if self.state == State.BURNING:
            self.fuel -= 1

    def is_burning(self) -> bool:
        return self.state == State.BURNING


if __name__ == "__main__":
    c = Cell(Type.CANYON)
    print(c)
    c.update()
    print(c)
    c.update(True)
    print(c)

    c.update()
    print(c)
