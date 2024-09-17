"""Setup for test suite."""

from collections.abc import Generator
from doctest import ELLIPSIS

import pytest
from beartype import beartype
from mock_vws import MockVWS
from mock_vws.database import VuforiaDatabase
from sybil import Sybil
from sybil.parsers.rest import (
    CaptureParser,
    DocTestParser,
    PythonCodeBlockParser,
)


@pytest.fixture(name="mock_vws")
def fixture_mock_vws() -> Generator[None, None, None]:
    """
    Yield a mock VWS.

    The keys used here match the keys in the documentation.
    """
    database = VuforiaDatabase(
        server_access_key="[server-access-key]",
        server_secret_key="[server-secret-key]",
        client_access_key="[client-access-key]",
        client_secret_key="[client-secret-key]",
    )
    # We use a low processing time so that tests run quickly.
    with MockVWS(processing_time_seconds=0.2) as mock:
        mock.add_database(database=database)
        yield


sybil_obj = Sybil(
    parsers=[
        DocTestParser(optionflags=ELLIPSIS),
        PythonCodeBlockParser(),
        CaptureParser(),
    ],
    patterns=["*.rst", "*.py"],
    fixtures=["mock_vws"],
)

pytest_collect_file = sybil_obj.pytest()


@beartype
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    Apply the beartype decorator to all collected test functions.
    """
    for item in items:
        if isinstance(item, pytest.Function):
            item.obj = beartype(obj=item.obj)
