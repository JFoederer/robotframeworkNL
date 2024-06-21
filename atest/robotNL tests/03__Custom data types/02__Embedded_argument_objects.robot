*** Keywords ***
Prepare boxes
    Take new Box
    Label the Box    Toy Box
    Put the following items in the Box    Teddy bear    Doll    Model car
    Take new Box
    Label the Box    Second box
    ${toy box}=    the box labeled    Toy Box
    ${second box}=    the box labeled    Second box
    Set Test Variable    ${toy box}
    Set Test Variable    ${second box}

*** Settings ***
Resource          base.resource

*** Test Cases ***
object from string conversion
    [Setup]    Prepare boxes
    Move all items from Toy Box into Second box
    Check That    the box labeled    Toy Box    Is Empty
    Check That    the box labeled    Second box    Contains 3 items

object from inline keyword
    [Setup]    Prepare boxes
    Using box    Toy Box
    Move all items from the box into Second box
    Check That    the box labeled    Toy Box    Is Empty
    Check That    the box labeled    Second box    Contains 3 items

object from variable
    [Setup]    Prepare boxes
    Move all items from ${toy box} into ${second box}
    Check That    the box labeled    Toy Box    Is Empty
    Check That    the box labeled    Second box    Contains 3 items

objects in operand keywords
    [Setup]    Prepare boxes
    Using box    Toy Box
    Check That    The item in Toy box that lies on top    Equals    Model car
    Check That    The item in the box that lies on top    Equals    Model car
    Check That    The item in ${toy box} that lies on top    Equals    Model car
