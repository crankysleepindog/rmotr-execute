from .commands import ExecutorCommand
from .languages import LANGUAGES_CONF
from . import exceptions


_cmd = ExecutorCommand(LANGUAGES_CONF)
execute = _cmd.execute
