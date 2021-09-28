import alembic.config
import os

here = os.path.dirname(os.path.abspath(__file__))
alembic_ini = os.path.join(here, "alembic.ini")

alembic_args = ["-c", alembic_ini, "upgrade", "head"]


def main():
    alembic.config.main(argv=alembic_args)
