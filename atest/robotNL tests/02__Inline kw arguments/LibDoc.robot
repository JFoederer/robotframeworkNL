*** Settings ***
Resource          base.resource
Library           libdoclib.py

*** Test Cases ***
Inline keywords are registered as type (standard docformat)
    Run Libdoc    docformat=robot
    Check that    libdoc registered types    Contains    InlineKeyword

Inline keywords are registered as type (markdown docformat)
    Run Libdoc    docformat=markdown
    Check that    libdoc registered types    Contains    InlineKeyword
