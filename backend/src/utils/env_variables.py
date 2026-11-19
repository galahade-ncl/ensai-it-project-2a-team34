import logging

import dotenv


def load_environment_variables():
    """
    Load environment variables from the ``.env`` file.

    Existing variables are overridden.

    Returns
    -------
    None
    """
    succes = dotenv.load_dotenv(override=True)
    logging.info(f"Load environment variables: {'SUCCES' if succes else 'FAIL'}")


def mask_value(key, value):
    """
    Mask sensitive values based on their key name.

    Parameters
    ----------
    key : str
        Name of the environment variable.
    value : str
        Actual value of the environment variable.

    Returns
    -------
    str
        ``'*******'`` if the key contains a sensitive keyword (PASSWORD,
        SECRET, KEY, TOKEN), otherwise the original value.
    """
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

    if any(word in key.upper() for word in sensitive_keywords):
        return "*******"
    return value


def display_values(include_prefix=None, exclude_prefix=None):
    """
    Log all environment variables, masking sensitive values.

    Parameters
    ----------
    include_prefix : str, optional
        If provided, only keys starting with this prefix are logged.
    exclude_prefix : str, optional
        If provided, keys starting with this prefix are skipped.

    Returns
    -------
    None
    """
    for key, value in dotenv.dotenv_values().items():
        if include_prefix and not key.startswith(include_prefix):
            continue
        if exclude_prefix and key.startswith(exclude_prefix):
            continue
        logging.info(f"{key}={mask_value(key, value)}")
