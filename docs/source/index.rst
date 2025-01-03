|project|
=========

Installation
------------

.. code-block:: shell

   pip install vws-auth-tools

This is tested on Python |minimum-python-version|\+.

Example usage
-------------


.. code-block:: python

   """Make a request to the VWS API."""

   import os
   from http import HTTPStatus
   from urllib.parse import urljoin

   import requests

   from vws_auth_tools import authorization_header, rfc_1123_date

   access_key = os.environ["VWS_SERVER_ACCESS_KEY"]
   secret_key = os.environ["VWS_SERVER_SECRET_KEY"]
   request_path = "/targets"
   content = b""
   method = "GET"
   formatted_date = rfc_1123_date()
   authorization_header_value = authorization_header(
       access_key=access_key,
       secret_key=secret_key,
       method=method,
       content=content,
       content_type="",
       date=formatted_date,
       request_path=request_path,
   )

   headers = {
       "Authorization": authorization_header_value,
       "Date": formatted_date,
   }

   response = requests.request(
       method=method,
       url=urljoin(base="https://vws.vuforia.com", url=request_path),
       headers=headers,
       data=content,
       timeout=30,
   )

   assert response.status_code == HTTPStatus.OK, response.text

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   contributing
   release-process
   changelog
