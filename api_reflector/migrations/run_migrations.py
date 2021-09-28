"""
Implements a simple command that invokes alembic with the correct paths.
This is helpful for running the migrations when the project is installed as a
package or docker container.
"""
import os

import alembic.config

here = os.path.dirname(os.path.abspath(__file__))
alembic_ini = os.path.join(here, "alembic.ini")

alembic_args = ["-c", alembic_ini, "upgrade", "head"]


def main():
    """
    Runs `alembic upgrade head`.
    """
    alembic.config.main(argv=alembic_args)
