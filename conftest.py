"""Setup for Sybil."""

from doctest import ELLIPSIS

from sybil import (
    Sybil,  # pyright: reportMissingTypeStubs=false,reportUnknownVariableType=false
)
from sybil.parsers.rest import (
    DocTestParser,
    PythonCodeBlockParser,
)

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=ELLIPSIS),
        PythonCodeBlockParser(),
    ],
    patterns=["*.rst", "*.py"],
).pytest()  # pyright: reportUnknownMemberType=false
