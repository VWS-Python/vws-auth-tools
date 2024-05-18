|project|
=========

Installation
------------

.. code:: sh

   pip install vws-auth-tools

This is tested on Python 3.12+.

Example usage
-------------

.. invisible-code-block: python

   from mock_vws import MockVWS
   from mock_vws.database import VuforiaDatabase

   mock = MockVWS(real_http=False)
   database = VuforiaDatabase(
       server_access_key='my_access_key',
       server_secret_key='my_secret_key',
       client_access_key='my_access_key',
       client_secret_key='my_secret_key',
   )
   mock.add_database(database=database)
   mock.__enter__()

.. code-block:: python

   from urllib.parse import urljoin

   import requests
   from vws_auth_tools import authorization_header, rfc_1123_date

   request_path = '/targets'
   content = b''
   method = 'GET'
   date = rfc_1123_date()
   authorization_header = authorization_header(
       access_key='my_access_key',
       secret_key='my_secret_key',
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

.. invisible-code-block: python

   mock.__exit__()

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   contributing
   release-process
   changelog
