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

   """Make a request to the VWS API."""

   request_path = "/targets"
   content = b""
   method = "GET"
<<<<<<< HEAD
   formatted_date = rfc_1123_date()
   authorization_header_value = authorization_header(
=======
   date = rfc_1123_date()
   authorization_header = authorization_header(
>>>>>>> 559660afacbbd34da66ef184efb594e94034f2a2
       access_key="[server-access-key]",
       secret_key="[server-secret-key]",
       method=method,
       content=content,
       content_type="",
<<<<<<< HEAD
       date=formatted_date,
       request_path=request_path,
   )

   headers = {"Authorization": authorization_header_value, "Date": formatted_date}
=======
       date=date,
       request_path=request_path,
   )

   headers = {"Authorization": authorization_header, "Date": date}
>>>>>>> 559660afacbbd34da66ef184efb594e94034f2a2

   response = requests.request(
       method=method,
       url=urljoin(base="https://vws.vuforia.com", url=request_path),
       headers=headers,
       data=content,
<<<<<<< HEAD
       timeout=30,
=======
>>>>>>> 559660afacbbd34da66ef184efb594e94034f2a2
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
