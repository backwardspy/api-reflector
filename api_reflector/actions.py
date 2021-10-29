"""
Contains types and methods related to rules engine actions.
"""
import json
import time
from enum import Enum

import requests

from api_reflector.reporting import get_logger

log = get_logger(__name__)


class Action(Enum):
    """
    Actions are optional extras that can be executed when a certain response is chosen.
    """

    DELAY = "DELAY"
    CALLBACK = "CALLBACK"

    def __str__(self) -> str:
        return self.value


def delay(*args, **_kwargs) -> None:
    time.sleep(float(args[0]))


def process_callback(*args, **kwargs):
    """
    send webhook or something to other app to process callback
    Params: args are currently a list of strings which for this callback process would be better as key values.
    Convert the args into a dict.
    """
    data_dict: dict[str, str] = {}

    for arg in args:
        split_vals = arg.split("=")
        data_dict[split_vals[0]] = split_vals[1]

    # Add the kwargs to the new data_dict to provide one dict to send in the request to the callback service
    data_dict.update(kwargs)

    try:
        requests.request("POST", url=data_dict["url"], data=json.dumps(data_dict))
    except requests.exceptions.RequestException as ex:
        log.warning(f"Check all Action arguments have been provided and that the callback service is running`{ex}`")


action_executors = {
    Action.DELAY: delay,
    Action.CALLBACK: process_callback,
}
