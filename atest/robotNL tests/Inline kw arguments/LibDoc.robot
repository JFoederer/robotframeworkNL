*** Settings ***
Resource          base.resource
Library           libdoclib.py

*** Test Cases ***
Inline keywords are registered as type
    Run Libdoc
    Check that    libdoc registered types    Contains    InlineKeyword
