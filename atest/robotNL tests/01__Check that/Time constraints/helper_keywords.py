from robot.api.deco import library, keyword


@library
class HelperKeywords:
    def __init__(self):
        self.gen = self._fail_fail_pass_generator()
        self.counter = 0

    @staticmethod
    def _fail_fail_pass_generator():
        yield False
        yield False
        yield True

    @keyword("Pass at the third attempt")
    def pass_at_third_attempt(self):
        return next(self.gen)

    @keyword("Reset counter")
    def reset_counter(self):
        self.counter = 0

    @keyword("counter increases, then pass")
    def plus_counter(self):
        self.counter += 1
        return True

    @keyword("counter value")
    def counter_value(self):
        return self.counter

    @keyword("1/100th of a second")
    def timespan_keyword(self):
        return '0.01 sec'

    @keyword("Not a timespan")
    def return_object(self):
        class MyObject:
            def __str__(self):
                return 'My object'
        return MyObject()
