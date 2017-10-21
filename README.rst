pythonanywhere-wrapper
==============

*A PythonAnywhere API wrapper.*

.. image:: https://travis-ci.org/cfc603/pythonanywhere-wrapper.png?branch=master
    :target: https://travis-ci.org/cfc603/pythonanywhere-wrapper

.. image:: https://codecov.io/github/cfc603/pythonanywhere-wrapper/coverage.svg?branch=master
    :target: https://codecov.io/github/cfc603/pythonanywhere-wrapper?branch=master

Usage
-----

::

    from pythonanywhere_wrapper.client import PythonAnywhere

    # If running on a PythonAnywhere terminal, your token and username will
    # be discovered automatically. Be sure to setup your API_TOKEN first.

    # For information on setting up your API_TOKEN visit
    # http://help.pythonanywhere.com/pages/API
    API_TOKEN = "test-token"

    # Your PythonAnywhere Username
    USER = "test-user"

    client = PythonAnywhere(api_key=API_TOKEN, user=USER)

Endpoints
---------

Consoles::

    # List all your consoles
    response = client.consoles()

    # View consoles shared with you
    response = client.consoles.shared_with_you()

    # Get console by id
    response = client.consoles(console_id=123456)

    # Kill a console by id
    response = client.consoles.delete(console_id=123456)

Files::

    # Start sharing a file
    response = client.files.sharing.create(data={"path": "/path/to/file"})

    # Get sharing status by path
    response = client.files.sharing(path="/path/to/file")

    # Stop sharing a file
    response = client.files.sharing.delete(path="/path/to/file")

    # List contents of a directory and subdirectories
    response = client.files.tree(path="/path/to/directory")

Webapps::

    # List all webapps
    response = client.webapps()

    # Create a new webapp
    response = client.webapps.create(data={
            "domain_name": "username.pythonanywhere.com",
            "python_version": "python27",
        })

    # Get webapp by domain name
    response = client.webapps(domain_name="username.pythonanywhere.com")

    # Modify config of a webapp. Follow with reloading webapp.
    response = client.webapps.update(
        domain_name="username.pythonanywhere.com", data={
            "python_version": "3.6",
            "virtualenv_path": "/path/to/virtualenv",
        }
    )

    # Delete webapp by domain name
    response = client.webapps.delete(domain_name="username.pythonanywhere.com")

    # Reload webapp
    response = client.webapps.reload(domain_name="username.pythonanywhere.com")

Static Files::

    # List all static files mappings for a domain
    response = client.webapps.static_files(
        domain_name="username.pythonanywhere.com"
    )

    # Create a new static file mapping for a domain. Reload webapp required.
    response = client.webapps.static_files.create(
        domain_name="username.pythonanywhere.com", data={
            "url": "/static/", "path": "/path/to/static/dir"
        }
    )

    # Get static file mapping by id
    response = client.webapps.static_files(
        domain_name="username.pythonanywhere.com", static_id=123
    )

    # Modify a static file mapping. Reload webapp required.
    response = client.webapps.static_files.update(
        domain_name="username.pythonanywhere.com", static_id=123, data={
            "url": "/static/", "path": "/path/to/static/dir"
        }
    )

    # Delete a static file mapping by id. Reload webapp required.
    response = client.webapps.static_files.delete(
        domain_name="username.pythonanywhere.com", static_id=123
    )

Credit
------

This application uses Open Source components. You can find the source code of their open source projects along with license information below. We acknowledge and are grateful to these developers for their contributions to open source.

:Project: chargify-python https://github.com/stevenwei/chargify-python
:Copyright: Copyright (c) 2010 Hindsight Labs
:License: (MIT) https://github.com/stevenwei/chargify-python/blob/master/LICENSE
