*** Settings ***
Resource          ../base.resource
Library           timed_keywords.py


*** Keywords ***
a delay of ${timespan} completes
    Sleep    ${timespan}
    RETURN    ${True}
