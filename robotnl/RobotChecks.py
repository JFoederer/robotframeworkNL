# BSD 3-Clause License
#
# Copyright (c) 2021, J. Foederer
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
log = logging.getLogger('top')

import time
from tkinter import messagebox, simpledialog, Tk

from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs, secs_to_timestr

class CheckFailed(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

class RobotChecks:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    def __init__(self):
        # Create and hide a Gui.
        # Enables the use for Tkiniter message boxes without displaying a main window
        root = Tk()
        root.withdraw()

    @staticmethod
    def __isKeyword(keywordCandidate):
        try:
            BuiltIn().keyword_should_exist(keywordCandidate)
        except AssertionError as error:
            if hasattr(error, 'message') and "multiple keywords" in error.message.lower():
                # The same AssertionError exception is raised when no keyword exists and when
                # multiple keywords with the same name exist. Therefore the text message is checked
                # as well.
                return True
            else:
                return False
        else:
            return True

    def check_precondition(self, *args):
        """
        Identical to `check that` but for use in precondition checks. Execution will not continue
        on failure.
        
        Precondition checks are used to validate assumptions made at the start of a test case or
        keyword. When a precondition check fails it indicates that the test case did not reach the
        point where it was able to check the requirement it was testing for.  
        """
        try:
            return RobotChecks.__execute_check("Precondition", *args)
        except CheckFailed as failure:
            failure.ROBOT_CONTINUE_ON_FAILURE = False
            raise failure            

    def check_postcondition(self, *args):
        """
        Identical to `check that` but for use in postcondition checks. Execution will not continue
        on failure.
        
        Postcondition checks are typically used in reusable keywords. They are added to assert that
        the expected result of the action was achieved successfully. A failing postcondition check
        causes the test case to fail, but indicates that the requirement it was testing for was not
        the cause of failure. 
        """
        try:
            return RobotChecks.__execute_check("Postcondition", *args)
        except CheckFailed as failure:
            failure.ROBOT_CONTINUE_ON_FAILURE = False
            raise failure            

    def check_that(self, *args):
        """
        Check that is used to validate data or state from the system under test.

        Check that takes values and/or robot keywords as input and evaluates the results. If the
        check fails it causes the test case to fail. If all keywords were executed correctly and
        only the check fails, the test will continue to execute remaining keywords and checks.
        
        Check that has two basic forms.
        - A single keyword (with its arguments) can be evaluated to a truth value
        - Two values or keywords (with their arguments) can be evaluated using an operator. It will
          then have the form Check that < ``keyword or value`` > < ``operator`` > < ``keyword or value`` >.

        Operator can be any Robot keyword taking exactly two values (left and right operands) as
        input. A number of predefined operators on numeric, string and list types are included in
        this library.        

        Examples:
        | `Check that` | 3 | `=` | 3 |
        | `Check that` | Two times | 6 | `equals` | 12 |
        | `Check that` | Two times | 5 | `≠` | Two times | 7 |
        | `Check that` | Earth exists |
        
        'Two times' in these examples is assumed to be defined as a Robot keyword that takes one
        argument and multiplies it by 2. Check that will pass if the evaluated result of Two times 9
        equals the fixed expected value 18.

        *Adding time constraints*:\n
                Any check can be extended with an additional timing constraint by adding ``within``
                This will cause the condition to be reevaluated until it becomes true, or until
                the specified time has passed. In the latter case the test case will fail.
                
        Example with time constraint:
        | `Check that` | condition is true | within | 1 minute 30 seconds |
        
        Elevator example:
        | `Check that` | elevator doors are closed |
        | Request elevator at floor | 3 |
        | `Check that` | elevator floor | `equals` | 3 | within | 20 seconds |
        | `Check that` | offset to floor level in mm | `≤` | 5 | within | 3 seconds | 
        """
        return RobotChecks.__execute_check("Requirement", *args)

    def check_manual(self, checkRequestText=""):
        """
        Suspends test execution to perform a manual or visual check.

        When used without arguments test execution is suspended until the tester clicks 'OK'.
        Optionally a question can be passed as argument that will be prompted for answering by the
        tester during test execution. Answering 'No' will cause the test case to fail.
        There is no timeout. Test execution is suspended indefinitely.
        """
        if checkRequestText:
            TesterVerdict = messagebox.askquestion("Check manual",
                    "Robot test execution suspended for manual check.\n\n%s" % checkRequestText)
            ReportString = "Manual check on '%s' [%s]" % (checkRequestText, TesterVerdict)
            if TesterVerdict == 'yes':
                BuiltIn().log(ReportString)
            else:
                raise CheckFailed(ReportString)

        else:
            messagebox.showinfo("Check manual", "Robot test execution suspended. Press OK to continue")

    def check_interactive(self):
        """
        Suspends test execution to accept manual input of keywords.
        
        A single ``Check interactive`` will repeatedly accept keyword input. Errors from keywords will
        not stop the test case, instead test execution continues until 'Cancel' is clicked or 'exit' is entered.
        There is no timeout. Test execution is suspended indefinitely.
        """
        exit = False
        exit_commands = {"exit", "quit", "stop", "e", "x", "q"}
        while not exit:
            newInput = simpledialog.askstring("Interactive keyword mode", "Enter a keyword. Arguments can be separated using multi-space. Type 'exit' or a blank keyword to exit interactive mode.")
            if newInput is None:
                exit = True
            elif newInput.lower() in exit_commands:
                exit = True
            elif len(newInput) != 0:
                BuiltIn().log("Interactive input: " + newInput)
                newInputSplit = list(filter(None, [s.strip() for s in newInput.replace('\t', '  ').split('  ')])) # Splits on double space, removes additional whitespace, then filters out empty elements
                # Unlike when "Run Keyword" is used in a .robot file, in "run_keyword()" the keyword must be explicitly split off from the arguments
                newKeyword = newInputSplit[0]
                newArgs = newInputSplit[1:]
                try:
                    BuiltIn().run_keyword(newKeyword, *newArgs)
                except Exception as e:
                    BuiltIn().log("Error in interactive keyword '%s'\n\n%s" % (newInput, e))

    @staticmethod
    def __execute_check(checkType, *args):
        """
        Parse arguments for check keyword to determine its operands, evaluate them and execute the
        check. 
        """
        Arguments = list(args)

        ############################################################################################
        # check for time argument
        TimeOutInSeconds = 0
        TimeRemaining = True
        s_TimeConstraint = ""
        if len(Arguments) >= 2 and str(Arguments[-2]).lower() == 'within':
            EvaluatedTimeArg = RobotChecks.__evaluateOperand([Arguments[-1]])[0]
            TimeOutInSeconds = timestr_to_secs(EvaluatedTimeArg)
            s_TimeConstraint = Arguments[-1] 
            Arguments = Arguments[:-2]

        if not len(Arguments):
            BuiltIn().fail("%s check failed. There was nothing to check." % checkType)

        ############################################################################################
        # Build expression
        LeftOperand = list()
        OperatorKeyword = None
        RightOperand = list()

        # Single argument or the first argument is a keyword AND No other arguments are keywords
        if len(Arguments) == 1 or \
                RobotChecks.__isKeyword(Arguments[0]) and not list(filter(RobotChecks.__isKeyword, Arguments[1:])):
            # Interpret as single boolean expression
            LeftOperand = Arguments

        else: # Interpret as expression
            LeftOperand.append(Arguments.pop(0))
    
            NextArgument = Arguments.pop(0)
            while not RobotChecks.__isKeyword(NextArgument):
                LeftOperand.append(NextArgument)

                # Prepare next loop
                if not len(Arguments):
                    BuiltIn().fail("Missing operator in check keyword")
                NextArgument = Arguments.pop(0)

            OperatorKeyword = NextArgument
            RightOperand = list(Arguments)

        ########################################################################################
        # Evaluate expression
        EvaluatedResult = None

        StartTime = time.perf_counter()
        TimeLeft = TimeOutInSeconds
        while EvaluatedResult != "passed" and TimeRemaining:
            EvaluationStartTime = time.perf_counter()
            if OperatorKeyword is None:
                BuiltIn().log("Evaluating boolean expression: %s" % (LeftOperand))
                # Evaluate boolean expression
                lValue, s_LeftOperand = RobotChecks.__evaluateOperand(LeftOperand)
                EvaluatedResult = "failed" if str(lValue).lower() != "true" else "passed" 

            else:
                lValue, s_LeftOperand = RobotChecks.__evaluateOperand(LeftOperand)
                if RightOperand:
                    rValue, s_RightOperand = RobotChecks.__evaluateOperand(RightOperand)
                    BuiltIn().log("Evaluating '%s' %s '%s'" % (lValue, OperatorKeyword, rValue))
                    EvaluatedResult = BuiltIn().run_keyword(OperatorKeyword, lValue, rValue)
                else:
                    BuiltIn().log("Evaluating '%s' '%s'" % (OperatorKeyword, lValue))
                    EvaluatedResult = BuiltIn().run_keyword(OperatorKeyword, lValue)

                EvaluatedResult = "failed" if str(EvaluatedResult).lower() != "true" else "passed" 

            EvaluationDuration = EvaluationStartTime - time.perf_counter()

            # Optimize timing
            TimeLeft = round((StartTime + TimeOutInSeconds) - time.perf_counter(), ndigits=3)
            TimeRemaining = TimeLeft >= 0 # include equal. Prevents failing on race conditions below 1ms accuracy.
            if EvaluatedResult != "passed" and TimeRemaining:
                if TimeOutInSeconds > 60:
                    if TimeLeft < 25 or TimeOutInSeconds - TimeLeft < 20:
                        # Speed up check cycle during the first and last parts of the waiting time
                        # During these periods the expectation of completing the action is highest
                        time.sleep(5)
                    else:
                        # Use a fixed delay time taking the actual processing time into account
                        # taking samples at fixed intervals regardless of performance
                        time.sleep(max(20 - EvaluationDuration, 0))

                elif TimeOutInSeconds > 15:
                    time.sleep(5) if TimeLeft > 7 else time.sleep(2)
                else:
                    time.sleep(1) if TimeLeft > 2 else time.sleep(.2)

        # Do reporting
        if OperatorKeyword is None:
            ReportString = "%s check on '%s'" % (checkType, s_LeftOperand)
        elif not RightOperand:
            ReportString = "%s check on '%s %s'" % (checkType, OperatorKeyword, s_LeftOperand)
        else:
            ReportString = "%s check on '%s %s %s'" % (checkType, s_LeftOperand, OperatorKeyword, s_RightOperand)

        if s_TimeConstraint:
            ActualTime = TimeOutInSeconds - TimeLeft
            if abs(TimeLeft) > 1 and ActualTime > 2:
                ActualTime = round(ActualTime) # skip ms detail for larger times
            ReportString += " after %s" % secs_to_timestr(ActualTime, compact=True)
            if not TimeRemaining and EvaluatedResult == "passed":
                ReportString += " (too late)"
                raise CheckFailed(ReportString)

        if EvaluatedResult == "passed":
            BuiltIn().log(ReportString)
        else:
            raise CheckFailed(ReportString)

    @staticmethod
    def __evaluateOperand(operand):
        # Create string variant of operands for reporting purposes
        s_Operand = " ".join([str(elm) for elm in operand])
        s_Value = str()

        if RobotChecks.__isKeyword(operand[0]):
            Value = BuiltIn().run_keyword(*operand)
            BuiltIn().log("'%s' is '%s'" % (s_Operand, Value))
            s_Value = str(Value)

        else:
            if len(operand) == 1:
                Value = BuiltIn().replace_variables(operand[0])
                if Value == operand[0]:
                    BuiltIn().log("Interpreting '%s' as fixed value" % s_Operand)
                else:
                    s_Value = str(Value)
                    BuiltIn().log("Interpreting '%s' as fixed value '%s'" % (s_Operand, s_Value))

            else:
                Value = list()
                for item in operand:
                    Value.append(BuiltIn().replace_variables(item))
                s_Value = str(Value)
                BuiltIn().log("Interpreting '%s' as list '%s'" % (s_Operand, s_Value))

        if s_Value:
            if len(s_Value) > 83:
                s_Value = s_Value[:40] + "..." + s_Value[-40:]

            s_Operand += " [%s]" % s_Value

        return Value, s_Operand
