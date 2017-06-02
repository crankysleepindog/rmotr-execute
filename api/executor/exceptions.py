class BaseExecutorException(Exception):
    pass


class InvalidLanguageFlavorException(BaseExecutorException):
    pass


class InvalidLanguageException(InvalidLanguageFlavorException):
    pass


class InvalidFlavorException(InvalidLanguageFlavorException):
    pass


class InvalidStrategyException(BaseExecutorException):
    pass


class TimeoutExecutorException(BaseExecutorException):
    pass
