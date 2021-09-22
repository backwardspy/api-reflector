"""
Converts a string into a slug.
"""

unsafe_chars = [
    '"',
    "#",
    "$",
    "%",
    "&",
    "+",
    ",",
    "/",
    ":",
    ";",
    "=",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "`",
    "{",
    "|",
    "}",
    "~",
    "'",
]


def slugify(text):
    """
    Creates a slug given a string with spaces, uppercase chars. Unsafe characters are removed Eg. %.
    """
    non_safe = [c for c in text if c in unsafe_chars]
    if non_safe:
        for char in non_safe:
            text = text.replace(char, "")
    text = u"-".join(text.split())
    return text.lower()
