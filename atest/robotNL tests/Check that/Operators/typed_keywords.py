# -*- coding: utf-8 -*-
from enum import Enum, IntEnum

from robot.api.deco import keyword, library


class Shape(Enum):
    TRIANGLE = 3
    RECTANGLE = 4


class Level(IntEnum):
    OFF = 0
    L1 = 1
    L2 = 2
    MAX = 3


class typed_keywords:
    @keyword("shape with ${n} sides")
    def shape_with_n_sides(self, n: int):
        return Shape(n)

    @keyword("Reset level")
    def reset(self):
        self.level = Level(0)

    @keyword("Increase level")
    def increase(self):
        if self.level.name != 'MAX':
            self.level = Level(self.level+1)

    @keyword("current level")
    def current_level(self):
        return self.level
