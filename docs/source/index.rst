|project|
=========

Installation
------------

.. code-block:: shell

   pip install vws-auth-tools

This is tested on Python |minimum-python-version|\+.

Example usage
-------------

VuMark Generation API
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Generate a VuMark instance."""

   import json
   import os
   from http import HTTPStatus
   from urllib.parse import urljoin

   import requests

   from vws_auth_tools import authorization_header, rfc_1123_date

   access_key = os.environ["VWS_SERVER_ACCESS_KEY"]
   secret_key = os.environ["VWS_SERVER_SECRET_KEY"]
   target_id = os.environ["VUMARK_TARGET_ID"]
   request_path = f"/targets/{target_id}/instances"
   content = json.dumps(obj={"instance_id": "123"}).encode()
   method = "POST"
   formatted_date = rfc_1123_date()
   authorization_header_value = authorization_header(
       access_key=access_key,
       secret_key=secret_key,
       method=method,
       content=content,
       content_type="application/json",
       date=formatted_date,
       request_path=request_path,
   )

   headers = {
       "Authorization": authorization_header_value,
       "Date": formatted_date,
       "Content-Type": "application/json",
       "Accept": "image/png",
   }

   response = requests.request(
       method=method,
       url=urljoin(base="https://vws.vuforia.com", url=request_path),
       headers=headers,
       data=content,
       timeout=30,
   )

   assert response.status_code == HTTPStatus.OK, response.text

Model Target Web API
~~~~~~~~~~~~~~~~~~~~

The `Model Target Web API`_ does not use the signature scheme which ``authorization_header`` implements.
It authenticates with OAuth2 client credentials: a ``POST /oauth2/token`` request with HTTP Basic credentials and a ``grant_type=client_credentials`` form body returns a bearer token, which is then sent to the dataset endpoints.

This package builds the headers only.
Making the token request, and caching the returned token until it expires, are left to you.

.. code-block:: python

   """Build authorization headers for the Model Target Web API."""

   import os

   from vws_auth_tools import (
       basic_authorization_header,
       bearer_authorization_header,
   )

   client_id = os.environ["VWS_MODEL_TARGET_CLIENT_ID"]
   client_secret = os.environ["VWS_MODEL_TARGET_CLIENT_SECRET"]

   token_request_headers = {
       "Authorization": basic_authorization_header(
           client_id=client_id,
           client_secret=client_secret,
       ),
       "Content-Type": "application/x-www-form-urlencoded",
   }

   # Sending ``grant_type=client_credentials`` to ``POST /oauth2/token``
   # with those headers returns JSON with an ``access_token`` item.
   access_token = "eyJhbGciOiJtb2NrIn0.e30.example-signature"  # noqa: S105

   dataset_request_headers = {
       "Authorization": bearer_authorization_header(
           access_token=access_token,
       ),
   }

   assert token_request_headers["Authorization"].startswith("Basic ")
   assert dataset_request_headers["Authorization"].startswith("Bearer ")

.. _Model Target Web API: https://developer.vuforia.com/library/vuforia-engine/web-api/model-target-web-api/

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   contributing
   release-process
   unreleased
   changelog
