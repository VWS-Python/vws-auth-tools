|project|
=========

Installation
------------

.. code-block:: shell

   pip install vws-auth-tools

This is tested on Python 3.12+.

Example usage
-------------

.. code-block:: python

   from urllib.parse import urljoin

   import requests
   from vws_auth_tools import authorization_header, rfc_1123_date

   request_path = '/targets'
   content = b''
   method = 'GET'
   date = rfc_1123_date()
   authorization_header = authorization_header(
       access_key='[server-access-key]',
       secret_key='[server-secret-key]',
       method=method,
       content=content,
       content_type='',
       date=date,
       request_path=request_path,
   )

   headers = {'Authorization': authorization_header, 'Date': date}

   response = requests.request(
        method=method,
        url=urljoin(base='https://vws.vuforia.com', url=request_path),
        headers=headers,
        data=content,
    )

   assert response.status_code == 200, response.text

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   contributing
   release-process
   changelog
