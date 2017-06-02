from .commands import ExecutorCommand
from .languages import LANGUAGES_CONF


_cmd = ExecutorCommand(LANGUAGES_CONF)
execute = _cmd.execute
