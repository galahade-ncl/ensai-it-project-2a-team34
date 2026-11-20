import logging
import logging.config
import numbers
from functools import wraps
from pathlib import Path

import yaml
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


def initialize_logs(name: str):
    """
    Initialize logging from the ``logging_config.yml`` configuration file.

    Creates the ``logs`` folder at the root of the project if it does
    not exist.

    Parameters
    ----------
    name : str
        Name of the application, written in the first log lines.

    Returns
    -------
    None
    """

    # Create the logs folder at project root if it doesn't exist
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(exist_ok=True)

    config_file = Path(__file__).resolve().parents[2] / "logging_config.yml"

    with open(config_file, encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
        logging.config.dictConfig(config)

        logging.info("-" * 50)
        logging.info(f"Starting {name}                           ")
        logging.info("-" * 50)


def get_logger(module_name: str, max_size: int = 25):
    """
    Return a logger with a shortened name based on the module path.

    If the path exceeds ``max_size``, the initials of the prefix parts
    are used (e.g. ``'s.f.file_service'``).

    Parameters
    ----------
    module_name : str
        Full name of the module (usually ``__name__``).
    max_size : int, default 25
        Maximum length of the name before it is shortened.

    Returns
    -------
    logging.Logger
        Logger with the (possibly shortened) name.
    """
    if len(module_name) <= max_size:
        return logging.getLogger(module_name)

    parts = module_name.split(".")
    short_prefix = [p[0] for p in parts[:-1]]
    short_name = ".".join(short_prefix + [parts[-1]])

    return logging.getLogger(short_name)


class LogIndentation:
    """
    Indent logs when entering a new method.

    Attributes
    ----------
    current_indentation : int
        Current indentation level.
    indentation_size : int
        Number of spaces per indentation level.
    """

    current_indentation = 0
    indentation_size = 2

    @classmethod
    def increase_indentation(cls):
        """
        Increase the indentation level by one.

        Returns
        -------
        None
        """
        cls.current_indentation += 1

    @classmethod
    def decrease_indentation(cls):
        """
        Decrease the indentation level by one.

        Returns
        -------
        None
        """
        cls.current_indentation -= 1

    @classmethod
    def get_indentation(cls):
        """
        Get the current indentation.

        Returns
        -------
        str
            Spaces corresponding to the current indentation level.
        """
        return " " * cls.indentation_size * cls.current_indentation


def log(func):
    """
    Decorator to log method calls and their outputs.

    When applied to a method, it logs the call with the parameter values
    (sensitive values such as passwords or keys are masked) and the
    return value of the method (shortened if too long).

    Parameters
    ----------
    func : callable
        Method to decorate.

    Returns
    -------
    callable
        Wrapped method.
    """

    SENSITIVE_KEYWORDS = {
        "password",
        "passwd",
        "pwd",
        "pass",
        "token",
        "secret",
        "key",
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], "__class__"):
            logger = get_logger(f"{args[0].__class__.__module__}")
        else:
            logger = logging.getLogger(__name__)

        LogIndentation.increase_indentation()
        indentation = LogIndentation.get_indentation()

        # Retrieve method parameters
        method_name = func.__name__
        param_names = func.__code__.co_varnames[1: func.__code__.co_argcount]
        args_list = []

        for i, arg in enumerate(args[1:]):
            if i >= len(param_names):
                break
            param_name = param_names[i].lower()
            if any(keyword in param_name for keyword in SENSITIVE_KEYWORDS):
                args_list.append("*****")
            else:
                args_list.append(str(arg) if not isinstance(arg, numbers.Number) else arg)

        for k, v in kwargs.items():
            if any(keyword in k.lower() for keyword in SENSITIVE_KEYWORDS):
                args_list.append("*****")
            else:
                args_list.append(str(v) if not isinstance(v, numbers.Number) else v)

        args_tuple = tuple(args_list)

        # Log method entry
        logger.info(f"{indentation}{method_name}{args_tuple} - START")
        result = func(*args, **kwargs)
        logger.info(f"{indentation}{method_name}{args_tuple} - END")

        # Shorten long output for readability
        if isinstance(result, list):
            result_str = str([str(item) for item in result[:3]])
            result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, dict):
            result_str = [(str(k), str(v)) for k, v in list(result.items())[:3]]
            result_str += f" ... ({len(result)} elements)"
        elif isinstance(result, str) and len(result) > 50:
            result_str = result[:50] + f" ... ({len(result)} characters)"
        else:
            result_str = str(result)

        logger.info(f"{indentation}  └─> Output: {result_str}")

        LogIndentation.decrease_indentation()

        return result

    return wrapper


class LogMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs every HTTP request and response.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Log an HTTP request and its response.

        Captures the method, the path, the status code and the error
        details.

        Parameters
        ----------
        request : Request
            Incoming HTTP request.
        call_next : callable
            Function that passes the request to the next handler.

        Returns
        -------
        Response
            Response returned by the next handler.

        Raises
        ------
        Exception
            Any exception raised while handling the request, re-raised
            after being logged.
        """

        method = request.method
        path = str(request.url.path)

        logging.info(f"{method} {path} - START")

        try:
            response = await call_next(request)
            logging.info(f"{method} {path} - END [Status: {response.status_code}]")
            return response

        except Exception as e:
            logging.error(f"{method} {path} - FAILED [Status: 500] Error: {str(e)}")
            raise e
