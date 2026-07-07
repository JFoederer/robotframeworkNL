*** Settings ***
Resource          ../base.resource
Library           helper_keywords.py


*** Keywords ***
a delay of ${timespan} completes
    Sleep    ${timespan}
    RETURN    ${True}
