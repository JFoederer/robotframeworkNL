*** Settings ***
Resource          base.resource

*** Test Cases ***
Fill a box
    Take new Box
    Put the following items in the Box    Teddy bear    Doll    Model car
    Check that    the Box    contains    Teddy bear

Label the box
    Take new Box
    Label the Box    Toy Box
    Put the following items in the Box    Teddy bear    Doll    Model car
    Check that    The Box Labeled    Toy box    Contains Item    Teddy bear

Custom sized box
    Take New Box    width=30    depth=30    height=30
    Check That    Volume Of Box    Equals    27000

Comparing box sizes
    Take New Box    width=30    depth=30    height=20
    Label The Box    Smaller box
    Take New Box    width=30    depth=30    height=40
    Label The Box    Taller box
    Check That    Volume Of Box    Smaller box    Equals    18000
    Check That    Volume Of Box    Taller box    Equals    36000
    Check That    Volume Of Box    Smaller box    <    Volume Of Box    Taller box
    Check That    The Box Labeled    Taller box    >    The Box Labeled    Smaller box
    Check That    The Box Labeled    Taller box    is greater than or equal to    The Box Labeled    Smaller box
    Comment    Using custom operator
    Check That    The Box Labeled    Taller box    is a larger box than    The Box Labeled    Smaller box
    Comment    Using automatic type conversion of custom operator
    Check That    Taller box    is a larger box than    Smaller box

Comparing box contents
    Take New Box
    Put The Following Items In The Box    Teddy bear
    Label The Box    Box A
    Take New Box
    Put The Following Items In The Box    Teddy bear
    Label The Box    Box B
    Check That    The Items In Box    Box A    contains exactly the items from    The Items In Box    Box B
    Put The Following Items In The Box    Doll
    Check That    The Number Of Items In Box    Box B    is greater than    The Number Of Items In Box    Box A
    Check That    Box B    contains more items than    Box A
    Using Box    Box A
    Put The Following Items In The Box    Model Car
    Check That    The Number Of Items In Box    Box A    equals    The Number Of Items In Box    Box B
    Move all items from Box A into Box B
    Check That    The Box Labeled    Box A    is empty
    Using Box    Box B
    Check that    The Box    contains 4 items

Similar boxes are not the same
    Take New Box
    Put The Following Items In The Box    Teddy bear    Doll    Model car
    Label The Box    Box A
    Take New Box
    Put The Following Items In The Box    Teddy bear    Doll    Model car
    Label The Box    Box B
    Check That    Volume Of Box    Box A    =    Volume Of Box    Box B
    Check That    The Items In Box    Box A    contains exactly the items from    The Items In Box    Box B
    Run Keyword And Expect Error    CheckFailed*    Check that    Box A    equals    Box B
