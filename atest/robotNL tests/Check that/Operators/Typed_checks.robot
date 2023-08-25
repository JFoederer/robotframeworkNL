*** Settings ***
Resource          base.resource
Library           typed_keywords.py

*** Test Cases ***
str comparisons
    Check that    one    equals    one
    Check that    ONE    equals    one
    Check that    ÖNé    equals    öné
    Check that    one    does not equal    two
    Check that    \ one \    does not equal    one

int comparisons
    Check that    1    equals    1
    Check that    ${1}    equals    ${1}
    Check that    ${1}    equals    1
    Check that    1    equals    ${1}
    Check that    ${1}    does not equal    11
    Check that    ${1}    does not equal    random text
    Check that    random text    does not equal    ${1}

float comparisons
    Check that    1.2    equals    1.2
    Check that    ${1.2}    equals    ${1.2}
    Check that    ${1/7}    equals    ${1/7}
    Check that    ${1.2}    equals    1.2
    Check that    1.20    equals    ${1.20}
    Check that    1    equals    ${1.0}
    Check that    ${1.0}    equals    1
    Check that    ${1.20}    equals    1.2
    Check that    1.20    equals    ${1.2}
    Check that    1.0    equals    ${1}
    Check that    ${1}    equals    1.0
    Check that    ${1.2}    does not equal    1.21
    Check that    ${1.2}    does not equal    random text

bool comparisons
    Check that    True
    Check that    ${True}
    Check that    True    equals    True
    Check that    True    equals    ${True}
    Check that    ${True}    equals    true
    Check that    false    equals    ${False}
    Check that    ${False}    equals    False
    Run Keyword And Expect Error    CheckFailed: Requirement check on 'False'    Check That    False
    Run Keyword And Expect Error    CheckFailed: Requirement check on 'False'    Check That    ${False}
    Run Keyword And Expect Error    CheckFailed: Requirement check on 'Random text'    Check That    Random text
    Run Keyword And Expect Error    CheckFailed: Requirement check on 'PASS'    Check That    PASS
    Run Keyword And Expect Error    CheckFailed: Requirement check on 'yes'    Check that    yes
    Check that    ${True}    does not equal    random text
    Check that    True    does not equal    yes
    Check that    ${true}    equals    yes
    Check that    ${False}    equals    no
    Check that    on    equals    ${True}
    Check that    off    equals    ${false}

enum comparisons
    Check that    shape with 3 sides    equals    shape with 3 sides
    ${triangle}=    shape with 3 sides
    Check that    ${triangle}    equals    shape with 3 sides
    Check that    shape with 3 sides    equals    TRIANGLE
    Check that    shape with 3 sides    equals    triANGLE
    Check that    TRIANGLE    equals    shape with 3 sides
    Check that    shape with 3 sides    does not equal    3
    Check that    shape with 3 sides    does not equal    shape with 4 sides

intenum comparisons
    Reset level
    Check that    current level    equals    current level
    Check that    current level    equals    0
    Check that    current level    equals    ${0}
    Check that    current level    equals    OFF
    Check that    current level    equals    off
    Check that    0    equals    current level
    Check that    ${0}    equals    current level
    Check that    OFF    equals    current level
    Check that    Off    equals    current level
    Increase level
    Increase level
    ${stored level}=    current level
    Check that    current level    equals    ${stored level}
    Check that    ${stored level}    equals    current level
    Check that    ${stored level}    equals    2
    Check that    ${stored level}    equals    ${2}
    Check that    ${stored level}    equals    L2
    Increase level
    Check that    current level    equals    MAX
    Check that    current level    does not equal    ${stored level}
    Check that    ${stored level}    is less than    current level
