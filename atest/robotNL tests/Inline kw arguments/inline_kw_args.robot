*** Settings ***
Resource          base.resource
Library           inline_kw_args.py

*** Test Cases ***
without typing
    Check that    twelve    equals    12
    ${value}=    echo    twelve
    Should be equal    ${value}    ${12}

with typing
    ${value}=    echo int    twelve
    Should be equal    ${value}    ${12}

with wrong type
    Run Keyword And Expect Error    REGEXP: .*cannot be converted to integer or keyword returning integer.    echo int    three quarters

string should stay a string
    ${value}=    echo    not a keyword
    Should be equal    ${value}    not a keyword

embedded arguments
    ${value}=    echo    multiply 'twelve' by 'three quarters'
    Should be equal    ${value}    ${9}
    ${value}=    echo    multiply '12' by 'three quarters'
    Should be equal    ${value}    ${9}
    ${value}=    echo    multiply '${12}' by 'three quarters'
    Should be equal    ${value}    ${9}
    Set suite variable    ${arg}    ${12}
    ${value}=    echo    multiply '${arg}' by 'three quarters'
    Should be equal    ${value}    ${9}
    Set suite variable    ${arg}    twelve
    ${value}=    echo    multiply '${arg}' by 'three quarters'
    Should be equal    ${value}    ${9}

args and kwargs
    ${value}=    named kwargs argument only    number=twelve
    Should be equal    ${value}    ${12}
