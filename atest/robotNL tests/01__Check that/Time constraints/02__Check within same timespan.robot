*** Settings ***
Resource          base.resource


*** Test Cases ***
The first check in a suite cannot refer to 'same timespan'
    Run keyword and expect error    *Joint timespan expected, but was not set*
    ...    Check that    ${True}    within    same timespan

Two checks pass within joint time constraint
    Check that    a delay of 10ms completes    within    100ms
    Check that    a delay of 10ms completes    within    same timespan

Second check fails the joint time constraint
    Check that    a delay of 10ms completes    within    100ms
    Run keyword and expect error    *too late*
    ...    Check that    a delay of 100ms completes    within    same timespan

A timespan can carry over to the next Test
    Run keyword and expect error    *too late*
    ...    Check that    a delay of 1ms completes    within    same timespan

A check without time constraint ends the running timespan
    Check that    a delay of 10ms completes    within    100ms
    Check that    ${True}
    Run keyword and expect error    *Joint timespan expected, but was not set*
    ...    Check that    a delay of 10ms completes    within    same timespan

Keywords do not affect the timespan of the Test
    Check that    a delay of 10ms completes    within    100ms
    Keyword that uses a shorter check within
    Check that    a delay of 50ms completes    within    same timespan

Keywords do not affect the timespan of other keywords
    Check that    a delay of 10ms completes    within    50ms
    Nested keyword that uses check within
    Check that    a delay of 10ms completes    within    same timespan


*** Keywords ***
Keyword that uses a shorter check within
    Check that    ${True}    within    10ms

Nested keyword that uses check within
    [Documentation]    Note that a check without 'within' would end a timespan
    ...                when used in the same scope.
    Check that    ${True}
    Keyword that uses a shorter check within
    Check that    ${True}
