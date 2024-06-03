*** Settings ***
Resource          base.resource

*** Test Cases ***
contains text operator
    Check that    the time is now    contains text    me
    Check that    the time is now    contains text    ME
    Check that    Françaisestraße    contains text    Straße
    Check that    Françaisestraße    contains text    Française
    Check that    Françaisestraße    contains text    Strasse
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    contains text    më
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    contains text    Francaise

contains exact text operator
    Check that    the time is now    contains exact text    me
    Check that    Françaisestraße    contains exact text    straße
    Check that    Françaisestraße    contains exact text    Française
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    contains exact text    ME
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    contains exact text    më
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    contains exact text    Francaise
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    contains exact text    strasse

does not contain text operator
    Check that    random text    does not contain text    my text
    Check that    the time is now    does not contain text    më
    Check that    Françaisestraße    does not contain text    Francaise
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not contain text    me
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not contain text    ME
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not contain text    the time is now
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    does not contain text    Straße
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    does not contain text    Française
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    does not contain text    Strasse

does not contain exact text operator
    Check that    random text    does not contain exact text    my text
    Check that    random text    does not contain exact text    RANDOM text
    Check that    the time is now    does not contain exact text    ME
    Check that    the time is now    does not contain exact text    më
    Check that    Françaisestraße    does not contain exact text    Francaise
    Check that    Françaisestraße    does not contain exact text    strasse
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not contain exact text    me
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    does not contain exact text    straße
    Run Keyword And Expect Error    CheckFailed*    Check that    Françaisestraße    does not contain exact text    Française

Matches text operators
    Check that    the time is now    matches with case to    the time is now
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    matches with case to    THE TIME IS NOW
    Check that    the time is now    matches without case to    THE TIME IS NOW
    Check that    Françaisestraße    matches with case to    Françaisestraße
    Check that    Françaisestraße    matches without case to    FRANÇAISESTRASSE
    Check that    random text    does not match without case to    my text
    Check that    random text    does not match with case to    RANDOM text
    Check that    the time is now    does not match with case to    THE TIME IS NOW
    Check that    the time is now    does not match with case to    the time
    Check that    the time is now    does not match without case to    the time
    Run Keyword And Expect Error    CheckFailed*    Check that    random text    does not match without case to    RANDOM text
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not match without case to    the time is now
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not match without case to    THE TIME IS NOW
    Run Keyword And Expect Error    CheckFailed*    Check that    the time is now    does not match with case to    the time is now
