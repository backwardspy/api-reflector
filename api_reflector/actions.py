"""
Contains types and methods related to rules engine actions.
"""
import json
import time
from datetime import datetime, timedelta
from enum import Enum

import requests

from api_reflector.reporting import get_logger
from api_reflector.storage import set_value_in_storage
from settings import settings

log = get_logger(__name__)


class Action(Enum):
    """
    Actions are optional extras that can be executed when a certain response is chosen.
    """

    DELAY = "DELAY"
    CALLBACK = "CALLBACK"
    STORE = "STORE"

    def __str__(self) -> str:
        return self.value


def delay(*args, **_kwargs) -> None:
    """
    Sleep for an amount of time.
    Takes a single positional argument; the number of seconds to sleep for.
    """
    length = float(args[0])

    if settings.maximum_delay_length is not None and length > settings.maximum_delay_length:
        log.warning(
            f"Delay length of {length} seconds exceeds maximum of {settings.maximum_delay_length} seconds. "
            "Delay will be clamped to the configured maximum."
        )
        length = min(length, settings.maximum_delay_length)

    time.sleep(length)


def process_callback(*args, **kwargs):
    """
    Sends a post request to a given URL.
    Takes arguments in key=value format. Requires one `url` argument to be set this way.
    Additional key=value arguments are sent to the given URL as a JSON payload.
    Request and response are also included in this request by default.
    """
    data_dict: dict[str, str] = {}

    for arg in args:
        split_vals = arg.split("=")
        data_dict[split_vals[0]] = split_vals[1]

    # Add the kwargs to the new data_dict to provide one dict to send in the request to the callback service
    data_dict |= kwargs

    try:
        requests.request("POST", url=data_dict["url"], data=json.dumps(data_dict), timeout=5)
    except requests.exceptions.RequestException as ex:
        log.warning(f"Check all Action arguments have been provided and that the callback service is running`{ex}`")


def set_value(*args, **kwargs):
    """
    Sets value for key specified in args into the storage object
    """
    key = args[0]
    value = args[1]
    endpoint = kwargs["endpoint"].rsplit("/", 1)[0]

    if settings.session_timeout:
        # FIXME: Could also allow expiry via action args. i.e delta = args[2]
        delta = settings.session_timeout
        expiry = datetime.now() + timedelta(minutes=int(delta))
        storage_value = {key: value, "expiry": expiry.timestamp()}
    else:
        storage_value = {
            key: value,
        }

    set_value_in_storage(key=endpoint, value=storage_value)


action_executors = {
    Action.DELAY: delay,
    Action.CALLBACK: process_callback,
    Action.STORE: set_value,
}
