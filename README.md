# robotframeworkNL - the oneliner
robotframeworkNL is a proving ground to boost Robot framework closer to Natural Language.

## Introduction
This project is an extension to [Robot framework](https://robotframework.org/) and although [Robot framework](https://robotframework.org/) made a very good step towards the goals of [keyword-driven testing ](https://en.wikipedia.org/wiki/Keyword-driven_testing) to make it readable for all stakeholders, there is still quite a lot of syntax involved that keeps test cases from really staying concise and to-the-point. In this project we will be introducing concepts to lift [Robot framework](https://robotframework.org/) to an even higher level.

This first release introduces ``Check that`` keywords that help to vastly reduce the amount of ``${...}`` cluttering in your test cases.

|**It let's you turn**||||||
|---|---|---|---|---|---|
| ${calculation 1}= | Two times    | ${6} ||||
| ${calculation 2}= | Three times  | ${4} ||||
| Should be equal   | ${calculation 1} |  ${calculation 2} ||||
|**into**||||||
| Check that | Two times | 6 | equals | Three times | 4 |

## Installation
The recommended installation method is using [pip](http://pip-installer.org)

    pip install --upgrade robotframework-nl

After installation include `robotnl` as library in your robot file to get access to the new keywords.  

## Documentation
[Link to keyword documentation](https://github.com/JFoederer/robotframeworkNL/blob/main/robotnl-libdoc.html) (if html does not render, choose *raw* format then right click to *save page as*)

Keyword documentation is in [libdoc](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#libdoc) format, making it also directly available via intellisense in the better IDEs, like [RIDE](https://github.com/robotframework/RIDE/wiki).

## Check that
This first release focuses around the *Check that* keywords. Using these keywords offers a large reduction in the need for variables in your test case and ``less variables=less ${} syntax``! It also encourages the use of the [Dovich](#dovich) principle, which is an easy way to create maintainable keyword libraries.

## Dovich
Dovich is short for Do-View-Check and the idea is simple, yet effective. Any keyword should have just one of these purposes, never more.
- Do keywords invoke an action and typically do not return anything
- View keyword make an observation and return this as a value. They typically do not change state.
- Check keywords are use for verifying information, typically the result of a view-keyword and an expected value. This `robotnl` library offers generic [Check keywords](#check-that) and operators. You can build new operator keywords in your own libraries to support any check you will ever need. 
