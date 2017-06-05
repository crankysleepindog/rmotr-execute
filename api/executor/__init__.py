from .commands import ExecutorCommand
from . import exceptions


_cmd = ExecutorCommand()
execute = _cmd.execute
