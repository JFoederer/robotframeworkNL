*** Settings ***
Resource          base.resource
Library           lib.py

*** Test Cases ***
without typing
    Check that    twelve    equals    12
    ${value}=    echo    twelve
    Should be equal    ${value}    ${12}

with typing
    ${value}=    echo typed    twelve
    Check that    ${value}    equals    12

with wrong type
    Run Keyword And Expect Error    REGEXP: .*cannot be converted to InlineKeyword or integer.    echo typed    three quarters

string should stay a string
    ${value}=    echo    not a keyword
    Check that    ${value}    equals    not a keyword

embedded arguments
    ${value}=    echo    multiply 'twelve' by 'three quarters'
    Check that    ${value}    equals    9
    ${value}=    echo    multiply '12' by 'three quarters'
    Check that    ${value}    equals    9
    ${value}=    echo    multiply '${12}' by 'three quarters'
    Check that    ${value}    equals    9
    Set suite variable    ${arg}    12
    ${value}=    echo    multiply '${arg}' by 'three quarters'
    Check that    ${value}    equals    9
    Set suite variable    ${arg}    twelve
    ${value}=    echo    multiply '${arg}' by 'three quarters'
    Check that    ${value}    equals    9
