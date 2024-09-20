"""Setup for test suite."""

import uuid
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
def fixture_mock_vws(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """
    Yield a mock VWS.

    The keys used here match the keys in the documentation.
    """
    server_access_key = uuid.uuid4().hex
    server_secret_key = uuid.uuid4().hex
    client_access_key = uuid.uuid4().hex
    client_secret_key = uuid.uuid4().hex

    database = VuforiaDatabase(
        server_access_key=server_access_key,
        server_secret_key=server_secret_key,
        client_access_key=client_access_key,
        client_secret_key=client_secret_key,
    )

    monkeypatch.setenv(name="VWS_SERVER_ACCESS_KEY", value=server_access_key)
    monkeypatch.setenv(name="VWS_SERVER_SECRET_KEY", value=server_secret_key)
    monkeypatch.setenv(name="VWS_CLIENT_ACCESS_KEY", value=client_access_key)
    monkeypatch.setenv(name="VWS_CLIENT_SECRET_KEY", value=client_secret_key)
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
