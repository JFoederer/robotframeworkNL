from robotnl import keyword
from robot.libraries.BuiltIn import BuiltIn;Robot = BuiltIn()

class Box:
    def __init__(self, width:int, depth:int, height:int):
        self.label = None
        self.width = width
        self.depth = depth
        self.height = height
        self.contents = []

    def __str__(self):
        return f"Box labeled {self.label}" if self.label else "unlabeled box"

    def __contains__(self, item):
        return item in self.contents

    def __iter__(self):
        return self.contents.__iter__()

    def __len__(self):
        return len(self.contents)

    def __eq__(self, other):
        return self is other

    def __gt__(self, other):
        return self.Volume > other.Volume

    def __ge__(self, other):
        return self.Volume >= other.Volume

    @property
    def Volume(self) -> int:
        return self.width * self.depth * self.height

def box_converter(value, library):
    if not isinstance(value, str):
        raise TypeError(f"Box type expected. Cannot convert {value} of type {type(value)} to box")
    try:
        BuiltIn().keyword_should_exist(value)
        result = BuiltIn().run_keyword(value)
        if isinstance(result, Box):
            return result
        raise TypeError()
    except:
        return Robot.run_keyword("the box labeled", value)

class Boxes:
    ROBOT_LIBRARY_CONVERTERS = {Box: box_converter}
    def __init__(self):
        self._boxes = {}
        self._active_box = None

    def the_box(self) -> Box:
        if self._active_box is None:
            raise Exception("Please take a box to confirm what 'the box' is")
        return self._active_box

    def using_box(self, label:str):
        self._active_box = self.the_box_labeled(label)

    def take_new_box(self, width=40, depth=50, height=30):
        self._active_box = Box(width, depth, height)

    def label_the_box(self, label:str):
        self._boxes[label.casefold()] = self._active_box
        self._active_box.label = label

    def the_box_labeled(self, label) -> Box:
        if label.casefold() not in self._boxes:
            raise ValueError(f"There is no box labeled {label}")
        return self._boxes[label.casefold()]

    def volume_of_box(self, box:Box="__active_box__") -> int:
        return self.the_box().Volume if box == "__active_box__" else box.Volume

    def the_number_of_items_in_box(self, box:Box) -> int:
        return len(box)

    @keyword("contains more items than")
    def more_items(self, this_box:Box, other_box:Box) -> bool:
        return len(this_box) > len(other_box)

    def the_items_in_box(self, box:Box) -> list:
        return box.contents

    @keyword("is a larger box than")
    def larger_box(self, this_box:Box, other_box:Box) -> bool:
        return this_box.Volume > other_box.Volume

    def put_the_following_items_in_the_box(self, *args):
        self._active_box.contents += [*args]

    @keyword("The item in ${box} that lies on top")
    def last_placed_item(self, box:Box):
        return box.contents[-1]

    @keyword("Move all items from ${boxA} into ${boxB}")
    def Move_items(self, boxA:Box, boxB:Box):
        Robot.log(f"Taking {boxA.contents} from {boxA}")
        Robot.log(f"Puting the items into {boxB}")
        boxB.contents += boxA.contents
        boxA.contents = []
