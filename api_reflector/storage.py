"""
Handle connections to supported k-v storage databases
"""
import pickledb

pickled = pickledb.load("pickle.db", auto_dump=True, sig=True)


def set_value_in_storage(key, value):
    """Sets key value in storage"""
    pickled.set(key, value)


def get_value_from_storage(key):
    """Gets value for a key from storage"""
    return pickled.get(key)
