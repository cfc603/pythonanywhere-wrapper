import getpass
import os
import requests

from pythonanywhere import API_ENDPOINT


# Maps certain function names to HTTP verbs
VERBS = {
    "create": "POST",
    "read": "GET",
    "update": "PUT",
    "delete": "DELETE"
}

# Map additional function name to HTTP verbs without removing them from path
ADDITIONAL_VERBS = {
    "reload": "POST",
}

# A list of identifiers that should be extracted and placed into the url
# string if they are passed into the kwargs.
IDENTIFIERS = {
    "console_id": "consoles",
    "domain_name": "webapps",
    "static_id": "static_files",
}


# Define exceptions
class PythonAnywhereError(Exception):
    pass


class PythonAnywhere(object):
    """
    A client for the PythonAnywhere API.
    """
    api_key = ""
    client = None
    user = None
    path = []

    def __init__(self, api_key=None, path=None, user=None):
        """
        :param api_key: The API key for your PythonAnywhere account.
        :param path: The current path constructed for this request.
        :param user: PythonAnywhere username
        :param client: The HTTP client to use to make the request.
        """
        self.api_key = api_key or os.environ["API_TOKEN"]
        self.path = path or []
        self.user = user or getpass.getuser()

    def __getattr__(self, attr):
        """
        Uses attribute chaining to help construct the url path of the request.
        """
        try:
            return object.__getattr__(self, attr)
        except AttributeError:
            return PythonAnywhere(self.api_key, self.path + [attr], self.user)

    def construct_request(self, **kwargs):
        """
        :param kwargs: The arguments passed into the request. Valid values are:
            "console_id", "domain_name", and "static_id" will be extracted and
            placed into the url. "data" will be passed seperately. Remaining
            kwargs will be passed as params into request.
        """
        path = self.path[:]

        # Find the HTTP method if we were called with create(), update(),
        # read(), or delete()
        if path[-1] in VERBS.keys():
            action = path.pop()
            method = VERBS[action]
        elif path[-1] in ADDITIONAL_VERBS.keys():
            method = ADDITIONAL_VERBS[path[-1]]
        else:
            method = "GET"

        # Extract certain kwargs and place them in the url instead
        for identifier, name in IDENTIFIERS.items():
            value = kwargs.pop(identifier, None)
            if value:
                path.insert(path.index(name)+1, str(value))

        # Need to pass data seperately from rest of kwargs
        data = kwargs.pop("data", None)

        # Build url
        url = API_ENDPOINT.format(self.user)
        url = url + "/".join(path) + "/"

        return url, method, data, kwargs

    def make_request(self, url, method, token, **kwargs):
        """
        Actually responsible for making the HTTP request.
        :param url: The URL to load.
        :param method: The HTTP method to use.
        :param token: PythonAnywhere API token found at
            https://www.pythonanywhere.com/user/USERNAME/account/#api_token
        :param kwargs: Values are passed into :class:`Request <Request>`
        """
        response = requests.request(
            method=method,
            url=url,
            headers={
                "Authorization": "Token {}".format(token),
                "User-Agent": "PythonAnywhere Python Client",
            },
            **kwargs
        )

        if not response.ok:
            raise PythonAnywhereError(
                "{} calling API: {}".format(
                    response.status_code, response.text
                )
            )

        return response

    def __call__(self, **kwargs):
        url, method, data, params = self.construct_request(**kwargs)
        return self.make_request(
            url, method, self.api_key, data=data, params=params
        )
