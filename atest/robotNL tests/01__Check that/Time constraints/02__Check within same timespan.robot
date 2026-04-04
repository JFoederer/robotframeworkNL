*** Settings ***
Resource          base.resource


*** Test Cases ***
The first check in a suite cannot refer to 'same timespan'
    TRY
        Check that    True    within    same timespan
    EXCEPT    Joint timespan expected, but was not set*    type=GLOB
        No Operation
    ELSE
        Fail    Expected fail did not occur
    END

Two checks pass within joint time constraint
    Check that    a delay of 10ms completes    within    100ms
    Check that    a delay of 10ms completes    within    same timespan

Second check passes, but not within the joint time constraint
    Check that    a delay of 10ms completes    within    100ms
    TRY
        Check postcondition    a delay of 100ms completes    within    same timespan
    EXCEPT    *too late*    type=GLOB
        No Operation
    ELSE
        Fail    Expected fail did not occur
    END

Setup new timespan to carry over to next test
    Comment    Setup only. Actual checks are executed in the next test.
    Check that    a delay of 10ms completes    within    100ms

A timespan can carry over to the next Test
    [Documentation]    Carry over of a timespan to the next test within a suite is
    ...    useful when you have an expensive action that has multiple asynchronous
    ...    results that you want to report and tag independently.
    Comment    Expects the running timespan from the previous test
    Check that    a delay of 10ms completes    within    same timespan
    TRY
        Check that    a delay of 90ms completes    within    same timespan
    EXCEPT    *too late*    type=GLOB
        Comment    Total delays add up to 110ms for the alotted 100ms.
    ELSE
        Fail    Expected fail did not occur
    END

A check without time constraint does not end the running timespan
    Check that    a delay of 10ms completes    within    100ms
    Check that    True
    Check that    a delay of 10ms completes    within    same timespan

Timespans can be reused inside control structures
    Check that    a delay of 10ms completes    within    100ms
    FOR    ${i}    IN RANGE    2
        Check that    a delay of 10ms completes    within    same timespan
    END

Checks after the timespan expired are executed exactly once
    Reset counter
    TRY
        Check that    ${False}    within    10ms
    EXCEPT    CheckFailed*    type=GLOB
        No Operation
    ELSE
        Fail    Expected fail did not occur
    END
    TRY
        Check that    counter increases, then pass    within    same timespan
    EXCEPT    *too late*    type=GLOB
        No Operation
    ELSE
        Fail    Expected fail did not occur
    END
    Check that    Counter value    equals    1

Keywords do not affect the timespan of the Test
    [Documentation]    The keyword that separates the check that sets the timespan
    ...    from the one using it, sets a new timnespan internally of just 10ms. If
    ...    If the timespans are not properly separated, the second check will fail
    ...    as 'too late'.
    Check that    a delay of 10ms completes    within    100ms
    Keyword that uses a shorter check within
    Check that    a delay of 20ms completes    within    same timespan

Keywords do not have access to the timespan of the calling test
    Check that    True    within    100ms
    TRY
        Keyword that tries to use existing timespan
    EXCEPT    Joint timespan expected, but was not set*    type=GLOB
        No Operation
    ELSE
        Fail    Expected fail did not occur
    END

Keywords do not affect the timespan of other keywords
    Check that    True    within    50ms
    Nested keyword that uses check within
    TRY
        Check that    True    within    same timespan
    EXCEPT    *too late*    type=GLOB
        Comment    Timespan already passed during the nested keyword
    ELSE
        Fail    Expected fail did not occur
    END


*** Keywords ***
Keyword that uses a shorter check within
    Check that    True    within    10ms

Keyword that tries to use existing timespan
    Check that    a delay of 10ms completes    within    same timespan

Nested keyword that uses check within
    Check that    a delay of 10ms completes    within    50ms
    Keyword that uses a longer check within
    TRY
        Check that    a delay of 50ms completes    within    same timespan
    EXCEPT    *too late**    type=GLOB
        Comment    Would not have failed if the longer timespan were set
    ELSE
        Fail    Expected fail did not occur
    END

Keyword that uses a longer check within
    TRY
        Check that    a delay of 10ms completes    within    same timespan
    EXCEPT    Joint timespan expected, but was not set*    type=GLOB
        Comment    Would not have failed if the calling keyword's timespan were accessable
    ELSE
        Fail    Expected fail did not occur
    END
    Check that    a delay of 10ms completes    within    1 second
    Check that    a delay of 10ms completes    within    same timespan
