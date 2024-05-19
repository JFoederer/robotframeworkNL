*** Settings ***
Resource          base.resource

*** Test Cases ***
Basic element checks
    @{empty_list}=    Create List
    @{animals}=    Create List    Bird    Wolf    Fish
    Check That    ${empty_list}    Is Empty
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Is Empty
    Check That    @{animals}    Counts 3 elements
    Check That    ${empty_list}    Counts 0 elements
    Check That    one    two    three    Counts 3 elements
    VAR    ${three}    3
    Check That    @{animals}    Counts ${three} elements
    Run Keyword And Expect Error    ValueError*    Check That    @{animals}    Counts three elements
    Check That    @{animals}    Contains    Wolf
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Contains    WOLF
    Check That    @{animals}    Contains Item    WOLF
    Check That    @{animals}    Does not contain    Platypus
    Check That    @{animals}    Does Not Contain Item    Platypus
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Does Not Contain Item    WOLF
    Check That    @{animals}    Contains Items    WOLF
    Check That    @{animals}    Contains Items    Fish    WOLF
    Check That    @{animals}    Contains Items    Fish    WOLF    WOLF
    Check That    @{animals}    Contains Items    @{animals}
    Check That    @{animals}    Contains Items    @{animals}    @{animals}    Fish
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Contains Items    Fish    Platypus
    Run Keyword And Expect Error    TypeError*    Check That    @{animals}    Does Not Contain Item    Fish    Platypus

Contains exactly the items from
    @{animals}=    Create List    Bird    Wolf    Fish
    Check that    ${animals}    Contains Exactly The Items From    Bird    Wolf    Fish
    Check that    ${animals}    Contains Exactly The Items From    Wolf    Fish    Bird
    Check that    ${animals}    Contains Exactly The Items From    ${animals}
    Check that    ${animals}    Contains Exactly The Items From    @{animals}
    Check that    @{animals}    Contains Exactly The Items From    @{animals}
    Check that    @{animals}    Contains Exactly The Items From    ${animals}
    @{short_list}=    Create List    Single element
    Check that    ${short_list}    Contains Exactly The Items From    Single element
    @{empty_list}=    Create List
    Check That    ${empty_list}    Contains Exactly The Items From    ${empty_list}
    Check that    Item1    Item2    Contains Exactly The Items From    Item2    Item1
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    Contains Exactly The Items From    Bird    Wolf
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    Contains Exactly The Items From    Bird    Wolf    Fish    Extra
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    Contains Exactly The Items From    ${short_list}
    Run Keyword And Expect Error    CheckFailed*    Check that    ${short_list}    Contains Exactly The Items From    @{animals}
    Run Keyword And Expect Error    CheckFailed*    Check that    ${empty_list}    Contains Exactly The Items From    Extra
    Run Keyword And Expect Error    CheckFailed*    Check that    Item1    Item2    Contains Exactly The Items From    ${empty_list}
