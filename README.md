# robotframeworkNL - the oneliner
robotframeworkNL is a proving ground to boost Robot framework closer to Natural Language.

## Introduction
This project is an extension to [Robot framework](https://robotframework.org/) and although [Robot framework](https://robotframework.org/) made a very good step towards the goals of [keyword-driven testing ](https://en.wikipedia.org/wiki/Keyword-driven_testing) to make it readable for all stakeholders, there is still quite a lot of syntax involved that keeps test cases from really staying concise and to-the-point. In this project we will be introducing concepts to lift [Robot framework](https://robotframework.org/) to an even higher level.

This second release introduces ``inline keywords`` and a set of  ``Check that`` keywords that help to vastly reduce the amount of ``${...}`` cluttering in your test cases. Combining these concepts helps to write a cleaner [Domain Specific Language](https://en.wikipedia.org/wiki/Domain-specific_language) around your [domain vocabulary](https://en.wikipedia.org/wiki/Jargon).

## Installation
The recommended installation method is using [pip](http://pip-installer.org)

    pip install --upgrade robotframework-nl

After installation include `robotnl` as library in your robot file to get access to the new keywords.

## Features

### Inline keywords

We use the term *inline keyword* when a keyword is used as an argument to another keyword. In this case the inline keyword must return a value, which will then be used as the actual argument. Consider this  basic example where a keywords exists by the name *'twelve'* that just returns the number 12, which is then used in an action keyword operating an elevator.

|**Using inline keyword**||
|---|---|
| Request elevator floor | twelve |
|**Traditional Robot**||
| ${floor to request}= | twelve |
| Request elevator floor | ${floor to request} |

To add support for inline keywords to your keywords, decorate your keyword with the `@keyword` decorator from the `robotnl` library, instead of using the one from `robot.api.deco`.

```python
from robotnl import keyword

    class my_elevator:
        @keyword(name="Request elevator floor")
        def handle_floor_request(target_floor):
            ...
```

Inline keywords are limited to a single *cell* in Robot. This means that keywords that are used inline, cannot take any positional arguments when used inline. Embedded arguments are considered part of the same cell and do not have that limitation.

Inline keywords are detected and processed at runtime. If a keyword is found that matches the argument's text, then that keyword will be executed and its return value used as the actual argument. When editing test cases, keyword highlighting can show which arguments are keywords when using a dynamic IDE like [RIDE](https://github.com/robotframework/RIDE/wiki) (one that loads the keyword libraries into the IDE). Static editors will not be able to show this information, due to the runtime evaluation.

### Check that

Using *Check that* keywords offers a large reduction in the need for variables in your test case and ``less variables = less ${} syntax``! It also encourages the use of the [Doobcheck](#doobcheck) principle, which is an easy way to create maintainable keyword libraries.

|**It let's you write**||||||
|---|---|---|---|---|---|
| Check that | Two times | 6 | equals | Three times | 4 |
|**instead of**||||||
| ${calculation 1}= | Two times    | ${6} ||||
| ${calculation 2}= | Three times  | ${4} ||||
| Should be equal   | ${calculation 1} |  ${calculation 2} ||||

### Time constraints

*Check that* offers support for executing checks that may take some time to complete. When using the optional `within` argument, followed by a time duration, *Check that* will apply *smart polling* to re-evaluate the expression and the keywords during the given period. Specifying the time limit is done using the standard [Robot Framework time format](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-176). It is advised to use a realistic time duration. This sets the correct expectation for the reader and helps robotnl optimise its polling algorithm.

|**Example using time constaints**||||||
|---|---|---|---|---|---|
| Request elevator at floor | 3 |||||
| Check that | elevator doors are closed | within | 20 seconds ||
| Check that | current elevator floor | equals | 3 | within | 1 minute |

### Hybrid manual testing

To manually interact with your automated test run during testing or test case development, robotnl offers the *Check manual* and *Check interactive* keywords. These keywords can be included at any point in the test case to suspend the test run at the current position for user input.

***Check Manual*** allows asking the tester a question. The question typically requests manual verification of an expected outcome. The answer will PASS or FAIL the test case, which is also reflected in the test report.

***Check interactive*** prompts the user to input a keyword. You have access to all build-in, user and library keywords available to that test case. The keyword is executed, but failures will not fail the test case nor abort execution. This is ideal for trying out keywords and keyword variations without having to restart the test run every time.

### Keyword documentation

Full documentation of the keywords offered by `robotnl` can be found here:  
[Link to keyword documentation](https://github.com/JFoederer/robotframeworkNL/blob/main/robotnl-libdoc.html) (if html does not render, choose *raw* format then right click to *save page as*)

Keyword documentation is in [libdoc](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#libdoc) format, making it also directly available via intellisense in IDEs, like [RIDE](https://github.com/robotframework/RIDE/wiki).

## Proposed improvements

* Option to mark keywords as *operator keywords*  
  This improvement affects the *Check that* keywords and will remove the limitations on using inline keywords as arguments to operands. Without annotating operator keywords as such, it is not always possible to detect which keywords are intended as arguments to the operand and which one should be the operator.
* Explicit literal support  
  Include a special annotation to express that something is not a keyword. For the odd case that a literal text needed as argument, also exists as a keyword. Alternativly the keyword receiving the argument can also use Robot's default keyword decorator.

## Doobcheck

Doobcheck is short for Do-Observe-Check and the idea is simple, yet effective. Any keyword should have just one of these purposes, never more.

- Do keywords invoke an action. These keywords start with a verb and do not return anything.
- Observation keywords return information, without affecting state. These keywords typically start with a noun, the thing that is being observed.
- Check keywords are used for verifying information, typically using the result of an observation-keyword and an expected value. This `robotnl` library offers generic [Check keywords](#check-that) and operators. You can build new operator keywords in your own libraries to support any check you will ever need.
