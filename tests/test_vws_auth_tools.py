"""Tests for authorization tools."""

import base64
import datetime
import hashlib
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time
from hypothesis import given
from hypothesis import strategies as st

import vws_auth_tools


def test_rfc_1123_date() -> None:
    """The date is returned in the format described in the VWS
    documentation.

    See https://developer.vuforia.com/library/web-api/vuforia-web-api-authentication:

    ```
    Date: This is the current date per RFC 2616, section 3.3.1, rfc1123-date
    format, for example, Sun, 22 Apr 2012 08:49:37 GMT,

    NOTE: The date and time always refer to GMT.
    ```
    """
    not_gmt_timezone = ZoneInfo(key="America/New_York")
    frozen_time = datetime.datetime(
        year=2015,
        month=2,
        day=5,
        hour=9,
        minute=55,
        second=12,
        microsecond=11,
        tzinfo=not_gmt_timezone,
    )
    with freeze_time(time_to_freeze=frozen_time):
        result = vws_auth_tools.rfc_1123_date()

    assert result == "Thu, 05 Feb 2015 14:55:12 GMT"


@pytest.mark.parametrize(
    argnames="content",
    argvalues=[b"some_bytes", "some_bytes"],
)
def test_authorization_header(content: bytes | str) -> None:
    """The Authorization header is constructed as documented.

    This example has been run on known-working code and so any refactor
    should continue to pass this test.
    """
    access_key = "my_access_key"
    # Ignore "Possible hardcoded password" as it is appropriate here.
    secret_key = "my_secret_key"  # noqa: S105
    method = "HTTPMETHOD"
    content_type = "some/content/type"
    date = "some_date_string"
    request_path = "/foo"

    result = vws_auth_tools.authorization_header(
        access_key=access_key,
        secret_key=secret_key,
        method=method,
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )

    assert result == "VWS my_access_key:8Uy6SKuO5sSBY2X8/znlPFmDF/k="


@pytest.mark.parametrize(argnames="content", argvalues=[b"", "", None])
def test_authorization_header_empty_content(
    content: bytes | str | None,
) -> None:
    """
    The Authorization header is the same for all empty content
    values.
    """
    access_key = "my_access_key"
    # Ignore "Possible hardcoded password" as it is appropriate here.
    secret_key = "my_secret_key"  # noqa: S105
    method = "HTTPMETHOD"
    content_type = "some/content/type"
    date = "some_date_string"
    request_path = "/foo"

    result = vws_auth_tools.authorization_header(
        access_key=access_key,
        secret_key=secret_key,
        method=method,
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )

    assert result == "VWS my_access_key:XXvKyRyMkwS8/1P1WLQ0duqNpKs="


@given(
    access_key=st.text(),
    secret_key=st.text(),
    method=st.text(),
    content=st.one_of(st.none(), st.binary(), st.text()),
    content_type=st.text(),
    date=st.text(),
    request_path=st.text(),
)
def test_authorization_header_is_deterministic(
    *,
    access_key: str,
    secret_key: str,
    method: str,
    content: bytes | str | None,
    content_type: str,
    date: str,
    request_path: str,
) -> None:
    """Valid inputs always produce the same valid HMAC-SHA1 signature."""
    first_result = vws_auth_tools.authorization_header(
        access_key=access_key,
        secret_key=secret_key,
        method=method,
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )
    second_result = vws_auth_tools.authorization_header(
        access_key=access_key,
        secret_key=secret_key,
        method=method,
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )

    assert first_result == second_result
    prefix = f"VWS {access_key}:"
    assert first_result.startswith(prefix)
    signature = first_result.removeprefix(prefix)
    digest_size = hashlib.sha1(usedforsecurity=False).digest_size
    assert len(base64.b64decode(s=signature, validate=True)) == digest_size


@given(content=st.text())
def test_authorization_header_encodes_unicode_content(content: str) -> None:
    """Unicode content is equivalent to its UTF-8 encoded bytes."""
    string_result = vws_auth_tools.authorization_header(
        access_key="my_access_key",
        secret_key="my_secret_key",  # noqa: S106
        method="HTTPMETHOD",
        content=content,
        content_type="some/content/type",
        date="some_date_string",
        request_path="/foo",
    )
    bytes_result = vws_auth_tools.authorization_header(
        access_key="my_access_key",
        secret_key="my_secret_key",  # noqa: S106
        method="HTTPMETHOD",
        content=content.encode(),
        content_type="some/content/type",
        date="some_date_string",
        request_path="/foo",
    )

    assert string_result == bytes_result
