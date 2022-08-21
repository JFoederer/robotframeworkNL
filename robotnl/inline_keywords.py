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

from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword as robot_keyword
from robot.api import logger

from functools import wraps
from typing import TypeVar, Generic, Union
from robot.running.arguments import TypeConverter


def is_keyword(keywordCandidate):
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

def evaluate_keyword_args(*args, **kwargs):
    converted_list = list()
    for arg in args:
        if is_keyword(arg):
            BuiltIn().log("Evaluating argument as keyword [%s]" % arg)
            converted_list.append(BuiltIn().run_keyword(arg))
            BuiltIn().log("%s → %s" % (arg, converted_list[-1]))
        else:
            converted_list.append(arg)

    converted_dict = dict()
    for k, v in kwargs.items():
        if is_keyword(arg):
            BuiltIn().log("Evaluating argument as keyword [%s]" % v)
            converted_dict[k] = BuiltIn().run_keyword(v)
            BuiltIn().log("%s = %s → %s" % (k, v, converted_dict[k]))
        else:
            converted_dict[k] = v

    return converted_list, converted_dict


class InlineKeyword(Generic[TypeVar('T')]):
    """
    Inline keywords are keywords that are used as argument to other keywords. The keyword will be
    evaluated and its return value used as the actual argument.
    """
    def __init__(self):
        self._name = f'keyword returning {self.__args__[0]}'

@TypeConverter.register
class InlineKeywordConverter(TypeConverter):
    type = InlineKeyword
    type_name = 'inline keyword'
    aliases = ('keyword', 'inline keyword')

    def __init__(self, type_, custom_converters=None):
        super().__init__(type_)
        self.nested_types = getattr(type_, '__args__', ())

    @property
    def type_name(self):
        return f'keyword returning {self.nested_types[0].__name__}' if self.nested_types else 'keyword'

    def _convert(self, value, explicit_type=True):
        if not is_keyword(value):
            raise ValueError
        BuiltIn().log("Evaluating argument as keyword [%s]" % value)
        result = BuiltIn().run_keyword(value)
        BuiltIn().log("%s → %s" % (value, result))
        if self.nested_types:
            converter = TypeConverter.converter_for(self.nested_types[0])
            if converter:
                result = converter.convert(str(result), result, explicit_type)
        return result

def keyword(name=None, tags=(), types=()):
    def decorator(func):
        for var, type_ in func.__annotations__.items():
            func.__annotations__[var] = Union[InlineKeyword[type_], type_]
        @robot_keyword(name, tags, types)
        @wraps(func)
        def wrapped(*args, **kwargs):
            converted_args, converted_kwargs = evaluate_keyword_args(*args, **kwargs)
            return func(*converted_args, **converted_kwargs)
        return wrapped
    return decorator
