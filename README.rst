|Build Status| |PyPI|

VWS Auth Tools
==============

Authentication and authorization tools for interacting with the Vuforia Web Services (VWS) API.

Installation
------------

.. code-block:: shell

   pip install vws-auth-tools

This is tested on Python |minimum-python-version|\+.

Usage
-----

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

Full Documentation
------------------

See the `full documentation <https://vws-python.github.io/vws-auth-tools/>`__.

.. |Build Status| image:: https://github.com/VWS-Python/vws-auth-tools/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/VWS-Python/vws-auth-tools/actions
.. |PyPI| image:: https://badge.fury.io/py/VWS-Auth-Tools.svg
   :target: https://badge.fury.io/py/VWS-Auth-Tools
.. |minimum-python-version| replace:: 3.13
