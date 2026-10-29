"""Setup for test suite."""

import uuid

# pytest-beartype evaluates fixture annotations at runtime.
from collections.abc import Generator  # noqa: TC003
from doctest import ELLIPSIS

import pytest
from mock_vws import MockVWS
from mock_vws.database import VuMarkDatabase
from mock_vws.target import VuMarkTarget
from sybil import Sybil
from sybil.parsers.rest import (
    CaptureParser,
    DocTestParser,
    PythonCodeBlockParser,
)


@pytest.fixture(name="mock_vws")
def fixture_mock_vws(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None]:
    """Yield a mock VWS.

    The keys used here match the keys in the documentation.
    """
    server_access_key = uuid.uuid4().hex
    server_secret_key = uuid.uuid4().hex
    target = VuMarkTarget(name="example-vumark")

    database = VuMarkDatabase(
        server_access_key=server_access_key,
        server_secret_key=server_secret_key,
        vumark_targets={target},
    )

    monkeypatch.setenv(name="VWS_SERVER_ACCESS_KEY", value=server_access_key)
    monkeypatch.setenv(name="VWS_SERVER_SECRET_KEY", value=server_secret_key)
    monkeypatch.setenv(name="VUMARK_TARGET_ID", value=target.target_id)
    monkeypatch.setenv(
        name="VWS_MODEL_TARGET_CLIENT_ID",
        value=uuid.uuid4().hex,
    )
    monkeypatch.setenv(
        name="VWS_MODEL_TARGET_CLIENT_SECRET",
        value=uuid.uuid4().hex,
    )
    # We use a low processing time so that tests run quickly.
    with MockVWS(processing_time_seconds=0.2) as mock:
        mock.add_vumark_database(vumark_database=database)
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
