WebServer Test
==============

How hard is it to stand up a simple web server in a few languages...

Installation
------------

On mac:

```bash
brew install python go
brew cask install java

# Install the python dependencies for test_it.py
pip install -r requirements.txt
```

Testing
-------

Verify a server implementation with:

```bash
python test_it.py
```

What does the server do?
------------------------

It accepts a GET request to root path, and return the following JSON:

```json
{
  "UTCDatetime": "<utc_datetime>",
  "UUID": "<random uuid>"
}
```

It also accepts a POST request that returns the same body, but accepts the UUID
as a URL parameter. E.g.

```http
POST /uuid/deadbeef-dead-beef-dead-beefdeadbeef
```

The uuid in the response will be the same as in the request URL.

The response should include the correct content type.
