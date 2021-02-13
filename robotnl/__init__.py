from .version import VERSION
from .RobotChecks import RobotChecks
from .CheckOperator import CheckOperator

class robotnl(RobotChecks, CheckOperator):
    """
    Generic non-domain specific keywords for use by all to enhance the Natural Language experience
    """

__version__ = VERSION
