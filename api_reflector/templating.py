"""
Defines the templating environment used for response content and rules.

Several filters are added into this environment. This module also defines a
default templating context, called `default_context`, that adds several useful
functions.

Some usage examples:

>>> {{ now() }}
2022-02-25T12:38:04.782273+00:00

>>> {{ now() | naive }}
2022-02-25T12:38:04.782273

>>> {{ now() | in_tz("Europe/Athens") }}
2022-02-25T14:38:04.782273+02:00

>>> {{ now() | dtformat("YYYY-MM-DD") }}
2022-02-25

>>> {{ now() + hours(10) }}
2022-02-25T22:38:04.782273+00:00

>>> {{ uuid() }}
a2dbcb56-161f-46ec-a8df-672b27c27281
"""
from uuid import uuid4

import pendulum
from jinja2 import Environment


def in_tz(datetime: pendulum.DateTime, timezone: str) -> pendulum.DateTime:
    """Convert the given datetime to a different timezone."""
    return datetime.in_tz(timezone)


def naive(datetime: pendulum.DateTime) -> pendulum.DateTime:
    """Strip timezone info from the given datetime."""
    return datetime.naive()


def dtformat(datetime: pendulum.DateTime, format_str: str) -> str:
    """Return the given datetime as a formatted string."""
    return datetime.format(format_str)


template_env = Environment()
template_env.filters["in_tz"] = in_tz
template_env.filters["naive"] = naive
template_env.filters["dtformat"] = dtformat


default_context = {
    # datetime utilities
    "now": lambda: pendulum.now("UTC"),
    "seconds": lambda n: pendulum.duration(seconds=n),
    "minutes": lambda n: pendulum.duration(minutes=n),
    "hours": lambda n: pendulum.duration(hours=n),
    "days": lambda n: pendulum.duration(days=n),
    "weeks": lambda n: pendulum.duration(weeks=n),
    "months": lambda n: pendulum.duration(months=n),
    "years": lambda n: pendulum.duration(years=n),
    # random data generators
    "uuid": lambda: str(uuid4()),
}
