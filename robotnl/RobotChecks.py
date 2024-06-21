# -*- coding: utf-8 -*-

# BSD 3-Clause License
#
# Copyright (c) 2022, J. Foederer
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

import time
try:
    import tkinter
    from tkinter import messagebox, simpledialog
except ImportError:
    tkinter = False

from robot.libraries.BuiltIn import BuiltIn
from robot.running import RUN_KW_REGISTER
from robot.utils import timestr_to_secs, secs_to_timestr
from .inline_keywords import is_keyword

class CheckFailed(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

class RobotChecks:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    def __init__(self):
        self.__gui = None

    @property
    def _gui(self):
        if self.__gui is not None or not tkinter:
            return self.__gui
        try:
            # Create and hide a Gui.
            # Enables the use for Tkiniter message boxes without displaying a main window
            root = tkinter.Tk()
            root.withdraw()
            self.__gui = True
        except:
            self.__gui = False
        return self.__gui

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
    RUN_KW_REGISTER.register_run_keyword('robotnl', check_precondition.__name__, args_to_process=0, deprecation_warning=False)

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
    RUN_KW_REGISTER.register_run_keyword('robotnl', check_postcondition.__name__, args_to_process=0, deprecation_warning=False)

    def check_that(self, *args):
        """
        Check that is used to validate data or state from the system under test.

        Check that takes values and/or robot keywords as input and evaluates the results. If the
        check fails it causes the test case to fail. If all keywords were executed correctly and
        only the check fails, the test will continue to execute remaining keywords and checks.

        Check that has two basic forms.
        - A single keyword (with its arguments) can be evaluated to a truth value
        - Two values or keywords (with their arguments) can be evaluated using an operator. It will
          then have the form Check that ``<keyword or value>`` ``<operator>`` ``<keyword or value>``.

        Operator can be any Robot keyword taking exactly two values (left and right operands) as
        input. A number of predefined operators on numeric, string and list types are included in
        this library.

        Examples:
        | `Check that` | 3 | `=` | 3 |
        | `Check that` | _Two times_ | 6 | `equals` | 12 |
        | `Check that` | _Two times_ | 5 | `≠` | _Two times_ | 7 |
        | `Check that` | _Earth exists_ |

        'Two times' in these examples is assumed to be defined as a Robot keyword that takes one
        argument and multiplies it by 2. `Check that` will pass if the evaluated result of _Two
        times_ 6 equals the fixed expected value 12.

        *Adding time constraints*:\n
                Any check can be extended with an additional timing constraint by adding ``within``
                This will cause the condition to be reevaluated until it becomes true, or until
                the specified time has passed. In the latter case the test case will fail.

        Example with time constraint:
        | `Check that` | _condition is true_ | within | 1 minute 30 seconds |

        Elevator example:
        | `Check that` | _elevator doors are closed_ |
        | _Request elevator at floor_ | 3 |
        | `Check that` | _elevator floor_ | `equals` | 3 | within | 20 seconds |
        | `Check that` | _offset to floor level in mm_ | `≤` | 5 | within | 3 seconds |
        """
        return RobotChecks.__execute_check("Requirement", *args)
    RUN_KW_REGISTER.register_run_keyword('robotnl', check_that.__name__, args_to_process=0, deprecation_warning=False)

    def check_manual(self, checkRequestText=""):
        """
        Suspends test execution to perform a manual or visual check.

        When used without arguments test execution is suspended until the tester clicks 'OK'.
        Optionally a question can be passed as argument that will be prompted for answering by the
        tester during test execution. Answering 'No' will cause the test case to fail.
        There is no timeout. Test execution is suspended indefinitely.
        """
        TesterVerdict = self.__prompt_user(checkRequestText)
        ReportString = "Manual check on '%s' [%s]" % (checkRequestText, TesterVerdict)
        if TesterVerdict == 'pass':
            BuiltIn().log(ReportString)
        elif TesterVerdict == 'fail':
            raise CheckFailed(ReportString)
        else:
            BuiltIn().log("Continued by user")

    def __prompt_user(self, message):
        if self._gui:
            if not message:
                messagebox.showinfo("Check manual", "Robot test execution suspended. Press OK to continue")
            else:
                TesterVerdict = messagebox.askquestion("Check manual",
                    "Robot test execution suspended for manual check.\n\n%s" % message)
                return 'pass' if TesterVerdict == 'yes' else 'fail'
        else:
            if not message:
                BuiltIn().log_to_console("\nRobot test execution suspended. Press ENTER to continue")
                input()
            else:
                BuiltIn().log_to_console("\nRobot test execution suspended for manual check."
                                          " (enter yes or y to pass)\n\n%s" % message)
                keys = input().lower()
                return 'pass' if keys == 'y' or keys == 'yes' else 'fail'

    def check_interactive(self):
        """
        Suspends test execution to accept manual input of keywords.

        A single ``Check interactive`` will repeatedly accept keyword input. Errors from keywords will
        not stop the test case, instead test execution continues until 'Cancel' is clicked or 'exit' is entered.
        There is no timeout. Test execution is suspended indefinitely.
        """
        exit = False
        exit_commands = {"exit", "quit", "stop", "e", "x", "q"}
        prompt = "Enter a keyword. Arguments can be separated using multi-space."\
                 " Type 'exit' or a blank keyword to exit interactive mode."
        while not exit:
            if self._gui:
                newInput = simpledialog.askstring("Interactive keyword mode", prompt)
            else:
                BuiltIn().log_to_console('\n'+prompt)
                newInput = input()
            if not newInput or newInput.lower() in exit_commands:
                exit = True
            elif len(newInput) != 0:
                BuiltIn().log_to_console("Interactive input: " + newInput)
                newInputSplit = list(filter(None, [s.strip() for s in newInput.replace('\t', '  ').split('  ')])) # Splits on double space, removes additional whitespace, then filters out empty elements
                # Unlike when "Run Keyword" is used in a .robot file, in "run_keyword()" the keyword must be explicitly split off from the arguments
                newKeyword = newInputSplit[0]
                newArgs = newInputSplit[1:]
                try:
                    return_value = BuiltIn().run_keyword(newKeyword, *newArgs)
                    if return_value is not None:
                        BuiltIn().log_to_console(return_value)
                except Exception as e:
                    BuiltIn().log_to_console("Error in interactive keyword '%s'\n\n%s" % (newInput, e))

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
           is_keyword(Arguments[0]) and not list(filter(is_keyword, Arguments[1:])):
            # Interpret as single boolean expression
            LeftOperand = Arguments

        else: # Interpret as expression
            LeftOperand.append(Arguments.pop(0))

            NextArgument = Arguments.pop(0)
            while not is_keyword(NextArgument):
                LeftOperand.append(NextArgument)

                # Prepare next loop
                if not len(Arguments):
                    BuiltIn().fail("Missing operator in check keyword")
                NextArgument = Arguments.pop(0)

            OperatorKeyword = NextArgument
            RightOperand = list(Arguments)

        ###########################################################################################
        # Evaluate expression
        EvaluatedResult = None

        StartTime = time.perf_counter()
        TimeLeft = TimeOutInSeconds
        PollMax = 20 # After 20s people start wondering: "Is it still going?" Time for an update.
        PollMin = min(PollMax/8, TimeOutInSeconds*3/100) # Shortest delay is 3% of the target time.
        PollDelay = PollMin # Initial poll delay will be 2x PollMin
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

            EvaluationDuration = time.perf_counter() - EvaluationStartTime

            # Optimize timing
            TimeLeft = round((StartTime + TimeOutInSeconds) - time.perf_counter(), ndigits=3)
            TimeRemaining = TimeLeft >= 0 if TimeOutInSeconds else False
                          # include equal to prevent failing on race conditions below 1ms accuracy.
            if EvaluatedResult != "passed" and TimeRemaining:
                # Polling cycle speeds up during the first and last parts of the waiting time. This
                # increases accuracy and response time in the more critical situations, without
                # causing an overload in polling and logging. For the maximum delay the evaluation
                # duration of the keyword is taken into account as well.
                PollDelay = min(TimeLeft/3, PollDelay*2)
                PollDelay = max(PollMin, min(PollDelay, PollMax)) # > min and < max
                time.sleep(max(PollDelay - EvaluationDuration, 0))

        # Do reporting
        if OperatorKeyword is None:
            ReportString = f"{checkType} check on '{s_LeftOperand}'"
        elif not RightOperand:
            ReportString = f"{checkType} check on '{OperatorKeyword} {s_LeftOperand}'"
        else:
            ReportString = f"{checkType} check on '{s_LeftOperand} {OperatorKeyword} {s_RightOperand}'"

        if s_TimeConstraint:
            ReportString += " within %s" % secs_to_timestr(TimeOutInSeconds)
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

        if is_keyword(operand[0]):
            Value = BuiltIn().run_keyword(*operand)
            BuiltIn().log(f"'{s_Operand}' is '{Value}'")
            s_Value = str(Value)

        else:
            if len(operand) == 1:
                Value = BuiltIn().replace_variables(operand[0])
                if Value == operand[0]:
                    BuiltIn().log(f"Interpreting '{s_Operand}' as fixed value", level='DEBUG')
                else:
                    s_Value = str(Value)
                    BuiltIn().log(f"Interpreting '{s_Operand}' as fixed value '{s_Value}'", level='DEBUG')

            else:
                Value = list()
                for item in operand:
                    Value.append(BuiltIn().replace_variables(item))
                s_Value = str(Value)
                BuiltIn().log(f"Interpreting '{s_Operand}' as list '{s_Value}'", level='DEBUG')

        if s_Value:
            if len(s_Value) > 83:
                s_Value = s_Value[:40] + "..." + s_Value[-40:]

            s_Operand += f" [{s_Value}]"

        return Value, s_Operand
