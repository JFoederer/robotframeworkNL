# -*- coding: utf-8 -*-

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

from robot.libraries.BuiltIn import BuiltIn

class CheckOperator:
    """
    This class defines a set of commonly used operators for use by 'Check that'
    and other check keywords
    """

    ################################################################################################
    # Generic operators that can work on basically any object type
    def equals(self, lValue, rValue):
        """Checks whether the left and right side are equal to each other [=]"""
        return OperatorProxy("==").basicOperator(lValue, rValue)

    def is_less_than(self, lValue, rValue):
        """Checks whether the left side is less than or smaller than the right side [<]"""
        return OperatorProxy("<").basicOperator(lValue, rValue)

    def is_greater_than(self, lValue, rValue):
        """Checks whether the left side is greater than or larger than the right side [>]"""
        return OperatorProxy(">").basicOperator(lValue, rValue)

    def is_less_than_or_equal_to(self, lValue, rValue):
        """Checks whether the left side is less than or equal to the right side [≤]"""
        return OperatorProxy("<=").basicOperator(lValue, rValue)

    def is_greater_than_or_equal_to(self, lValue, rValue):
        """Checks whether the left side is greater than or equal to the right side [≥]"""
        return OperatorProxy(">=").basicOperator(lValue, rValue)

    def does_not_equal(self, lValue, rValue):
        """Checks whether the left side is different from the right side [≠]"""
        return OperatorProxy("!=").basicOperator(lValue, rValue)

    ################################################################################################
    # Operators that work on text items str() or Unicode()
    def contains_text(self, baseString, subString):
        """Performs a case insensitive check whether the right side is a substring of the left side"""
        try:
            return self.contains_exact_text(baseString.lower(), subString.lower())
        except:
            return False

    def contains_exact_text(self, baseString, subString):
        """Performs a case sensitive check whether the right side is a substring of the left side"""
        try:
            return subString in baseString
        except:
            return False

    def matches_without_case_to(self, leftText, rightText):
        """Performs a case insensitive check whether the left and right side texts are equal"""
        try:
            return self.matches_with_case_to(leftText.lower(), rightText.lower())
        except:
            return False

    def matches_with_case_to(self, leftText, rightText):
        """Performs a case sensitive check whether the left and right side texts are equal"""
        return leftText == rightText

    def does_not_contain_text(self, baseString, subString):
        """Performs a case insensitive check whether the right side is not a substring of the left side"""
        return not self.contains_text(baseString, subString)

    def does_not_contain_exact_text(self, baseString, subString):
        """Performs a case sensitive check whether the right side is not a substring of the left side"""
        return not self.contains_exact_text(baseString, subString)

    def does_not_match_without_case_to(self, leftText, rightText):
        """Performs a case insensitive check whether the left and right side texts are different"""
        return not self.matches_without_case_to(leftText, rightText)

    def does_not_match_with_case_to(self, leftText, rightText):
        """Performs a case sensitive check whether the left and right side texts are different"""
        return not self.matches_with_case_to(leftText, rightText)

    ################################################################################################
    # Operators that work on lists or other sequences
    def is_empty(self, iterable):
        return len(iterable) == 0

    def contains(self, iterable, part):
        """Checks whether part is present in iterable. Uses primitive 'in' operator."""
        return part in iterable

    def does_not_contain(self, iterable, part):
        """Checks whether part is present in iterable. Uses primitive 'not in' operator."""
        return part not in iterable

    def contains_item(self, sequence, part):
        """
        Checks whether the right side item is part of the sequence on the left side.
        Iterates over the sequence to apply automatic Robot type conversion where applicable.
        """
        for item in sequence:
            BuiltIn().log("Processing '%s' from list" % item)
            if self.is_equal_to(part, item):
                BuiltIn().log("Matched")
                return True
            BuiltIn().log("No match")
        return False

    def contains_exactly_the_items_from(self, sequence, sequence_right):
        """
        Checks whether the sequence on the right side contains all items of the left side and vice versa.
        Iterates over sequence on the left and matches each element with a single element on the right. 
        """
        for item in sequence:
            item_found_in_parts = False
            BuiltIn().log("Processing '%s' from list" % item)
            for i in range(len(sequence_right)):
                if self.equals(sequence_right[i],item):
                    sequence_right.pop(i)
                    item_found_in_parts = True
                    break
            if not item_found_in_parts:
                BuiltIn().log("Item '%s' from left side is not found in the list on the right side" % item)
                return False
        if len(sequence_right) > 0:
            BuiltIn().log("Not all items from right side list are present: %s" % sequence_right)
            return False

        return True

    def does_not_contain_item(self, sequence, part):
        """
        Checks whether the right side item is not part of the sequence on the left side.
        Iterates over the sequence to apply automatic Robot type conversion where applicable.
        """
        return not self.contains_item(sequence, part)

# Add operator keywords that do not comply to Python's identifier syntax
setattr(CheckOperator, "=", CheckOperator.equals)
setattr(CheckOperator, "<", CheckOperator.is_less_than)
setattr(CheckOperator, ">", CheckOperator.is_greater_than)
setattr(CheckOperator, "≤", CheckOperator.is_less_than_or_equal_to)
setattr(CheckOperator, "≥", CheckOperator.is_greater_than_or_equal_to)
setattr(CheckOperator, "≠", CheckOperator.does_not_equal)

class OperatorProxy:
    """
    Proxy class for mapping generic Robot comparison keywords to Python operators 
    """
    def __init__(self, s_operator):
        self.__s_Operator = s_operator

    @staticmethod
    def __typeCastRobotStringValue(leadingValue, otherValue):
        """
        Robot arguments are always passed as string even when comparing numbers or other objects.
        When a string argument is detected the other argument is deemed leading. This function
        converts the other argument to the leading value's type when possible. Otherwise the value
        is kept unchanged, inevitably leading to a mismatch in comparison.
        
        Precondition: otherValue is of types str and supports .lower()
        returns type casted otherValue
        """
        CastedOther = otherValue # By default leave untouched 
        if type(leadingValue) is int:
            BuiltIn().log("Comparing as integer values")
            try:
                CastedOther = int(otherValue)
            except ValueError:
                pass

        elif type(leadingValue) is float:
            BuiltIn().log("Comparing as floating point values")
            try:
                CastedOther = float(otherValue)
            except ValueError:
                pass

        elif type(leadingValue) is bool:
            BuiltIn().log("Comparing as boolean values")
            if otherValue.lower() == "true":
                CastedOther = True
            if otherValue.lower() == "false":
                CastedOther = False

        else:
            # By default compare as case insensitive Unicode. Note that it already was a string.
            BuiltIn().log("Interpreting '%s' as string (case insensitive)" % otherValue)
            CastedOther = str(otherValue).lower() 

        return CastedOther

    def basicOperator(self, lvalue, rvalue):
        # Local argument copies for assignment
        lValue = lvalue
        rValue = rvalue

        if type(lvalue) is str:
            lValue = OperatorProxy.__typeCastRobotStringValue(rvalue, lvalue)

        if type(rvalue) is str:
            rValue = OperatorProxy.__typeCastRobotStringValue(lvalue, rvalue)

        if lValue is lvalue and rValue is rvalue:
            BuiltIn().log("Comparing evaluated keyword values")

        return eval("lValue %s rValue" % self.__s_Operator)                        
