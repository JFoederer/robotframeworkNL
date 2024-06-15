*** Settings ***
Resource          base.resource

*** Test Cases ***
Basic item checks
    @{empty_list}=    Create List
    @{animals}=    Create List    Bird    Wolf    Fish
    Check that    ${empty_list}    is empty
    Run Keyword And Expect Error    CheckFailed*    Check that    @{animals}    is empty
    Check that    @{animals}    contains 3 items
    Check that    ${empty_list}    contains 0 items
    @{single}=    Create List    one
    Check that    ${single}    contains 1 item
    Check that    one    two    three    contains 3 items
    VAR    ${three}    3
    Check that    @{animals}    contains ${three} items
    Run Keyword And Expect Error    ValueError*    Check that    @{animals}    contains three items
    Check that    @{animals}    contains    Wolf
    Run Keyword And Expect Error    CheckFailed*    Check that    @{animals}    contains    WOLF
    Run Keyword And Expect Error    CheckFailed*    Check that    @{animals}    contains    Bird    Wolf
    Check that    @{animals}    contains item    WOLF
    Check that    @{animals}    does not contain    Platypus
    Check that    @{animals}    does not contain item    Platypus
    Run Keyword And Expect Error    CheckFailed*    Check that    @{animals}    does not contain item    WOLF
    Check that    @{animals}    contains items    WOLF
    Check that    @{animals}    contains items    Fish    WOLF
    Check that    @{animals}    contains items    Fish    WOLF    WOLF
    Check that    @{animals}    contains items    @{animals}
    Check that    @{animals}    contains items    @{animals}    @{animals}    Fish
    Run Keyword And Expect Error    CheckFailed*    Check that    @{animals}    contains items    Fish    Platypus
    Run Keyword And Expect Error    TypeError*    Check that    @{animals}    does not contain item    Fish    Platypus
    @{numbers}=    Create List    ${3}    ${2}    ${1}
    Check that    @{numbers}    contains    ${3}
    Run Keyword And Expect Error    CheckFailed*    Check that    @{numbers}    contains    3
    Check that    @{numbers}    contains item    3
    Check that    @{numbers}    contains item    1    ${2.0}    3

contains exactly the items from
    @{animals}=    Create List    Bird    Wolf    Fish
    Check that    ${animals}    contains exactly the items from    Bird    Wolf    Fish
    Check that    ${animals}    contains exactly the items from    Wolf    Fish    Bird
    Check that    ${animals}    contains exactly the items from    BIRD    WOLF    FISH
    Check that    ${animals}    contains exactly the items from    ${animals}
    Check that    ${animals}    contains exactly the items from    @{animals}
    Check that    @{animals}    contains exactly the items from    @{animals}
    Check that    @{animals}    contains exactly the items from    ${animals}
    @{short_list}=    Create List    Single item
    Check that    ${short_list}    contains exactly the items from    Single item
    @{empty_list}=    Create List
    Check that    ${empty_list}    contains exactly the items from    ${empty_list}
    Check that    item1    item2    contains exactly the items from    item2    item1
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    contains exactly the items from    Bird    Wolf
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    contains exactly the items from    Bird    Wolf    Fish    Extra
    Run Keyword And Expect Error    CheckFailed*    Check that    ${animals}    contains exactly the items from    ${short_list}
    Run Keyword And Expect Error    CheckFailed*    Check that    ${short_list}    contains exactly the items from    @{animals}
    Run Keyword And Expect Error    CheckFailed*    Check that    ${empty_list}    contains exactly the items from    Extra
    Run Keyword And Expect Error    CheckFailed*    Check that    item1    item2    contains exactly the items from    ${empty_list}
