*** Settings ***
Resource          base.resource

*** Test Cases ***
All basic operators are available as text
    Check that    1    equals    1
    Check that    1    does not equal    2
    Check that    1    is less than    2
    Check that    2    is greater than    1
    Check that    1    is less than or equal to    1
    Check that    1    is greater than or equal to    1

All basic operators are available as symbol
    Check that    1    =    1
    Check that    1    ≠    2
    Check that    1    <    2
    Check that    2    >    1
    Check that    1    ≤    1
    Check that    1    ≥    1
