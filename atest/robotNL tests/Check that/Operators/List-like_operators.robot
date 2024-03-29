*** Settings ***
Resource          base.resource

*** Test Cases ***
Basic element checks
    @{empty_list}=    Create List
    Check That    ${empty_list}    Is Empty
    @{animals}=    Create List    Bird    Wolf    Fish
    Check That    @{animals}    Contains    Wolf
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Contains    WOLF
    Check That    @{animals}    Contains Item    WOLF
    Check That    @{animals}    Does not contain    Platypus
    Check That    @{animals}    Does Not Contain Item    Platypus
    Run Keyword And Expect Error    CheckFailed*    Check That    @{animals}    Does Not Contain Item    WOLF

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
