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

from robot.api import TypeInfo
from robot.libraries.BuiltIn import BuiltIn
from robot.running.arguments import TypeConverter
from robot.utils import is_list_like

from .inline_keywords import keyword

class CheckOperator:
    """
    This class defines a set of commonly used operators for use by 'Check that'
    and other check keywords
    """

    ################################################################################################
    # Generic operators that can work on basically any object type
    def equals(self, lValue, rValue):
        """Checks whether the left and right side are equal to each other [`=`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 7 | `=` | 7 |
        | `Check that` | ${7} | `=` | 7.0 |
        | `Check that` | _Two times_ | 6 | `equals` | 12 |
        | `Check that` | text | `equals` | TeXT |
        """
        return OperatorProxy("==").basicOperator(lValue, rValue)

    def is_less_than(self, lValue, rValue):
        """Checks whether the left side `is less than` or smaller than the right side [`<`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 2 | `<` | 4 |
        | `Check that` | 2 | `is less than` | 4 |
        """
        return OperatorProxy("<").basicOperator(lValue, rValue)

    def is_greater_than(self, lValue, rValue):
        """Checks whether the left side `is greater than` or larger than the right side [`>`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 4 | `>` | 2 |
        | `Check that` | 4 | `is greater than` | 2 |
        """
        return OperatorProxy(">").basicOperator(lValue, rValue)

    def is_less_than_or_equal_to(self, lValue, rValue):
        """Checks whether the left side `is less than or equal` to the right side [`≤`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 2 | `≤` | 2 |
        | `Check that` | 2 | `is less than or equal to` | 4 |
        """
        return OperatorProxy("<=").basicOperator(lValue, rValue)

    def is_greater_than_or_equal_to(self, lValue, rValue):
        """Checks whether the left side `is greater than or equal to` the right side [`≥`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 4 | `≥` | 4 |
        | `Check that` | 4 | `is greater than or equal to` | 2 |
        """
        return OperatorProxy(">=").basicOperator(lValue, rValue)

    def does_not_equal(self, lValue, rValue):
        """Checks whether the left side `does not equal`, i.e. is different from the right side [`≠`]

        Applies Robot type conversions when executing the check.
        Examples:
        | `Check that` | 7 | `≠` | 13 |
        | `Check that` | 7 | `≠` | 7.01 |
        | `Check that` | _Two times_ | 6 | `does not equal` | 13 |
        | `Check that` | random text | `does not equal` | my text |
        """
        return OperatorProxy("!=").basicOperator(lValue, rValue)

    ################################################################################################
    # Operators that work on text items str() or Unicode()
    def contains_text(self, baseString, subString):
        """Performs a case insensitive check whether the right side is a substring of the left side

        Examples:
        | `Check that` | the time is now | `contains text` | me |
        | `Check that` | the time is now | `contains text` | ME |
        | `Check That` | Robotstraße | `contains text` | Strasse |
        """
        try:
            return self.contains_exact_text(baseString.casefold(), subString.casefold())
        except:
            return False

    def contains_exact_text(self, baseString, subString):
        """Performs a case sensitive check whether the right side is a substring of the left side

        Examples:
        | `Check that` | the time is now | `contains text` | me |
        | `Check That` | Robotstraße | `contains text` | straße |
        """
        try:
            return subString in baseString
        except:
            return False

    def matches_without_case_to(self, leftText, rightText):
        """Performs a case insensitive check whether the left and right side texts are equal

        Examples:
        | `Check that` | the time is now | `matches without case to` | the time is now |
        | `Check that` | the time is now | `matches without case to` | THE TIME IS NOW |
        | `Check That` | Robotstraße | `matches without case to` | ROBOTstrasse |
        """
        try:
            return self.matches_with_case_to(leftText.casefold(), rightText.casefold())
        except:
            return False

    def matches_with_case_to(self, leftText, rightText):
        """Performs a case sensitive check whether the left and right side texts are equal

        Examples:
        | `Check that` | the time is now | `matches with case to` | the time is now |
        | `Check That` | Robotstraße | `matches with case to` | Robotstraße |
        """
        return leftText == rightText

    def does_not_contain_text(self, baseString, subString):
        """Performs a case insensitive check whether the right side is not a substring of the left side

        Examples:
        | `Check that` | random text | `does not contain text` | my text |
        """
        return not self.contains_text(baseString, subString)

    def does_not_contain_exact_text(self, baseString, subString):
        """Performs a case sensitive check whether the right side is not a substring of the left side

        Examples:
        | `Check that` | random text | `does not contain exact text` | my text |
        | `Check that` | random text | `does not contain exact text` | RANDOM text |
        """
        return not self.contains_exact_text(baseString, subString)

    def does_not_match_without_case_to(self, leftText, rightText):
        """Performs a case insensitive check whether the left and right side texts are different

        Examples:
        | `Check that` | random text | `does not match without case to` | my text |
        """
        return not self.matches_without_case_to(leftText, rightText)

    def does_not_match_with_case_to(self, leftText, rightText):
        """Performs a case sensitive check whether the left and right side texts are different

        Examples:
        | `Check that` | random text | `does not match with case to` | my text |
        | `Check that` | random text | `does not match with case to` | RANDOM text |
        """
        return not self.matches_with_case_to(leftText, rightText)

    ################################################################################################
    # Operators that work on lists or other sequences
    def is_empty(self, iterable):
        """Checks whether the sequence on the left does not contain any elements

        Example:
        | Take new shopping cart |
        | `Check that` | shopping cart | `is empty` |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        return len(iterable) == 0

    @keyword("counts ${n} elements")
    def counts_n_elements(self, n:int, iterable):
        """Checks whether the sequence on the left counts ${n} elements

        Example:
        | `Check precondition` | shopping cart | `is empty` |
        | Add 1 cube to shopping cart |
        | Add 1 sphere to shopping cart |
        | `Check that` | shopping cart | `counts 2 elements` |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        count = len(iterable)
        BuiltIn().log(f"Counted {count} elements")
        return count == n

    def contains(self, iterable, part):
        """Checks whether part is present in iterable. Uses Python's primitive in-operator.

        Example:
        | Add 1 cube to shopping cart |
        | Add 1 sphere to shopping cart |
        | `Check that` | shopping cart | `contains` | cube |
        | `Check that` | shopping cart | `contains` | sphere |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        return part in iterable

    def does_not_contain(self, iterable, part):
        """Checks whether part is present in iterable. Uses Python's primitive 'not in' operator.

        Example:
        | `Check precondition` | shopping cart | `is empty` |
        | Add 1 cube to shopping cart |
        | `Check that` | shopping cart | `does not contain` | sphere |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        return part not in iterable

    def contains_item(self, sequence, part):
        """Checks whether the right side item(s) is/are part of the sequence on the left side.

        `Contains item` and the plural `Contains items` are aliases. The difference with `Contains`
        is that these iterate over the sequence and applies *automatic Robot type conversion*
        between elements when applicable. Duplicate items from the right side can match a single
        item from the left side.

        Example:
        | Add 2 cubes to shopping cart |
        | Add 1 sphere to shopping cart |
        | `Check that` | shopping cart | `contains item` | cube |
        | `Check that` | shopping cart | `contains items` | sphere | cube |
        | `Check that` | shopping cart's price list | `contains items` | 2.50 | ${1.99} |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        if not is_list_like(part):
            part = [part]
        for elem in part:
            BuiltIn().log(f"Processing '{elem}' from right side")
            for item in sequence:
                if self.equals(elem, item):
                    BuiltIn().log("Matched")
                    break
                BuiltIn().log("No match")
            else:
                BuiltIn().log(f"{elem} not present in left side list")
                return False
        return True

    # Alias for plural form
    contains_items = contains_item

    def contains_exactly_the_items_from(self, sequence, sequence_right):
        """
        Checks whether the sequence on the right side contains all items of the left side and vice versa.
        Iterates over sequence on the left and matches each element with a single element on the right.
        The items can be in any order.

        Example:
        | `Check precondition` | shopping cart | `is empty` |
        | Add 2 cubes to shopping cart |
        | Add 1 sphere to shopping cart |
        | `Check that` | shopping cart | `contains exactly the items from` | cube | cube | sphere |
        | `Check that` | shopping cart | `contains exactly the items from` | cube | sphere | cube |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        if isinstance(sequence_right, str):
            sequence_right = [sequence_right]
        sequence_right = [*sequence_right]
        for item in sequence:
            BuiltIn().log(f"Processing '{item}' from left side list")
            for i in range(len(sequence_right)):
                if self.equals(item, sequence_right[i]):
                    sequence_right.pop(i)
                    break
            else:
                BuiltIn().log(f"Item '{item}' from left side is not found in the list on the right side")
                return False
        if len(sequence_right) > 0:
            BuiltIn().log(f"Not all items from right side list are present: {sequence_right}")
            return False

        return True

    def does_not_contain_item(self, sequence, part):
        """
        Checks whether the right side item is not part of the sequence on the left side.
        Iterates over the sequence and applies automatic Robot type conversion where applicable.

        No plural variant is available for this keyword due to ambiguity with List-like values. When
        writing "[2, 4, 6] does not contain items [4, 5, 6]", one could expect a pass, because the
        set [4, 5, 6] is not contained, but also a fail because item 4 *is* part of the left side set.

        Example:
        | `Check precondition` | shopping cart | `is empty` |
        | Add 1 cube to shopping cart |
        | `Check that` | shopping cart | `does not contain item` | sphere |
        _Assumes a 'shopping cart' type to be defined with associated action and observation keywords._
        """
        if is_list_like(part):
            raise TypeError("List-like items not accepted as right side value")
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
    def __typeCastRobotStringValue(leadingValue, otherValue, name):
        """
        When Robot files are parsed, arguments are always passed as string even when comparing
        numbers or other objects. When a string argument is detected the other argument is
        deemed leading. This function converts the other argument to the leading value's type
        when possible. Otherwise the value is kept unchanged, inevitably leading to a mismatch
        in comparison.

        Precondition: otherValue is of types str and supports .casefold()
        returns type casted otherValue
        """
        CastedOther = otherValue # By default leave untouched
        converter = TypeConverter.converter_for(TypeInfo.from_type(type(leadingValue)))
        if converter:
            try:
                CastedOther = converter.convert(otherValue, name)
            except ValueError as err:
                BuiltIn().log(err, level='DEBUG')
            BuiltIn().log(f"Comparing as {converter.type_name} values")

        if isinstance(CastedOther, str):
            # By default compare as case insensitive Unicode. Note that it already was a string.
            BuiltIn().log(f"Interpreting {name} '{otherValue}' as string (case insensitive)")
            CastedOther = str(otherValue).casefold()

        return CastedOther

    def basicOperator(self, lvalue, rvalue):
        # Local argument copies for assignment
        lValue = lvalue
        rValue = rvalue

        if type(lvalue) is str:
            lValue = OperatorProxy.__typeCastRobotStringValue(rvalue, lvalue, "left operand")

        if type(rvalue) is str:
            rValue = OperatorProxy.__typeCastRobotStringValue(lvalue, rvalue, "right operand")

        if lValue is lvalue and rValue is rvalue:
            BuiltIn().log("Comparing values as is")

        return eval(f"lValue {self.__s_Operator} rValue")
