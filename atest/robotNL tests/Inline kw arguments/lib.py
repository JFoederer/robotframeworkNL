from robot.api.deco import library
from robotnl import keyword
#from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn;Robot = BuiltIn()

@library
class lib:
    @keyword(name="twelve")
    def fake_name(self):
        return 12

    @keyword(name="three quarters")
    def three_quarters(self):
        return .75

    @keyword(name="echo")
    def mirror(self, arg):
        return arg
        
    @keyword(name="echo typed")
    def mirror_typed(self, arg:int):
        return arg

    @keyword(name="arg stuff")
    def arg_stuff(self, one, two='two', three='three'):
        Robot.log_many(one, two, three)

    @keyword(name="multiply '${x}' by '${y}'")
    def multiply(self, x: int, y: float):
        return x * y

    @keyword(name="Named kwargs argument only")
    def named_args_only(self, **kwargs):
        if 'number' not in kwargs:
            raise AssertionError("named argument number expected")
        if type(kwargs['number']) is not int:
            raise AssertionError("kwarg number must be an int")
        return kwargs['number']
