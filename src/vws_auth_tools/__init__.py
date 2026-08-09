"""Authorization helpers."""

import base64
import email.utils
import hashlib
import hmac

from beartype import beartype


@beartype
def _compute_hmac_base64(*, key: bytes, data: bytes) -> bytes:
    """
    Return the Base64 encoded HMAC-SHA1 hash of `data` using the
    `key`.
    """
    hashed = hmac.new(key=key, msg=None, digestmod=hashlib.sha1)
    hashed.update(msg=data)
    return base64.b64encode(s=hashed.digest())


@beartype
def rfc_1123_date() -> str:
    """Return the date formatted as per RFC 2616, section 3.3.1,
    rfc1123-date.

    This is the date needed by the VWS API, as described in
    https://developer.vuforia.com/library/web-api/vuforia-web-api-authentication.
    """
    return email.utils.formatdate(timeval=None, localtime=False, usegmt=True)


@beartype
def authorization_header(
    *,
    access_key: str,
    secret_key: str,
    method: str,
    content: str | bytes | None,
    content_type: str,
    date: str,
    request_path: str,
) -> str:
    """Get an `Authentication` header for the VWS API.

    This can be used for a request made to the VWS API with the given
    attributes.

    See https://developer.vuforia.com/library/web-api/vuforia-web-api-authentication.

    Args:
        access_key: A VWS server or client access key.
        secret_key: A VWS server or client secret key.
        method: The HTTP method which will be used in the request.
        content: The request body which will be used in the request.
        content_type: The `Content-Type` header which is expected by
            endpoint. This does not necessarily have to match the
            `Content-Type` sent in the headers. In particular, for the query
            API, this must be set to `multipart/form-data` but the header must
            include the boundary.
        date: The current date which must exactly match the date sent in the
            `Date` header.
        request_path: The path to the endpoint which will be used in the
            request.

    Returns:
        An `Authorization` header which can be used for a request made
        to the VWS API with the given attributes.
    """
    hashed = hashlib.md5(usedforsecurity=False)

    if content is None:
        content = b""

    if isinstance(content, str):
        content = content.encode(encoding="utf-8")

    hashed.update(content)
    content_md5_hex = hashed.hexdigest()

    components_to_sign = [
        method,
        content_md5_hex,
        content_type,
        date,
        request_path,
    ]
    string_to_sign = "\n".join(components_to_sign)
    signature = _compute_hmac_base64(
        key=secret_key.encode(),
        data=string_to_sign.encode(),
    )
    return f"VWS {access_key}:{signature.decode()}"


@beartype
def basic_authorization_header(*, client_id: str, client_secret: str) -> str:
    """Get an `Authorization` header for an OAuth2 token request.

    The Model Target Web API does not use the VWS signature scheme which
    `authorization_header` implements.  Instead, a token is requested from
    ``POST /oauth2/token`` with ``grant_type=client_credentials`` and HTTP
    Basic credentials, and the returned bearer token is then sent to the
    dataset endpoints with `bearer_authorization_header`.

    Performing the token request, and caching the returned token, are left
    to the caller.

    See https://developer.vuforia.com/library/vuforia-engine/web-api/model-target-web-api/.

    Args:
        client_id: A Model Target Web API client ID.
        client_secret: A Model Target Web API client secret.

    Returns:
        An `Authorization` header which can be used for a request made to
        the Model Target Web API token endpoint.
    """
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(
        s=credentials.encode(encoding="utf-8"),
    )
    return f"Basic {encoded_credentials.decode(encoding='ascii')}"


@beartype
def bearer_authorization_header(*, access_token: str) -> str:
    """Get an `Authorization` header for a Model Target Web API request.

    This is used for requests to the Model Target Web API dataset
    endpoints, with an access token obtained from a token request made with
    `basic_authorization_header`.

    See https://developer.vuforia.com/library/vuforia-engine/web-api/model-target-web-api/.

    Args:
        access_token: An access token returned by the Model Target Web API
            token endpoint.

    Returns:
        An `Authorization` header which can be used for a request made to
        the Model Target Web API dataset endpoints.
    """
    return f"Bearer {access_token}"
