*** Settings ***
Resource          base.resource


*** Test Cases ***
Single action passes within time span
    Check that    a delay of 10ms completes    within    1 second

Polling action passes within time span
    Check that    pass at the third attempt    within    2 seconds

Keyword passes, but too late
    Run keyword and expect error    *too late*
    ...                             Check that    a delay of 500ms completes    within    100ms

Single action fails after time span
    ${message}=    Run keyword and expect error    CheckFailed*
    ...            Check that    a delay of 200ms completes    equals    ${False}    within    100ms
    Check that     ${message}    does not contain text    too late

Polling action keeps failing within time span
    Run keyword and expect error    CheckFailed*
    ...                             Check that    Apple    equals    Pear    within    100ms

Invalid time string
    Run keyword and expect error    *Invalid time string*
    ...                             Check that    ${True}    within    the blink of an eye
