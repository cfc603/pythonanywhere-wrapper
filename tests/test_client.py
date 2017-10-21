import pytest
import responses

from pythonanywhere_wrapper import API_ENDPOINT
from pythonanywhere_wrapper.client import PythonAnywhereError


class PythonAnywhereTestCase(object):

    API_ENDPOINT = API_ENDPOINT.format("testuser")

    def asserts(self, expected_url, method="GET", data=None):
        assert len(responses.calls) == 1
        call = responses.calls[0]
        assert call.response.url == self.get_url(expected_url)
        assert call.request.method == method
        if data:
            for argument in data:
                assert argument in call.response.request.body

    def get_url(self, url):
        return self.API_ENDPOINT + url


class TestMakeRequest(PythonAnywhereTestCase):

    @responses.activate
    def test_make_request(self, api_client):
        responses.add(responses.GET, self.get_url("consoles/"))
        api_client.consoles()

        assert len(responses.calls) == 1
        call = responses.calls[0]
        headers = call.request.headers
        assert headers["Authorization"] == "Token api_key"
        assert headers["User-Agent"] == "PythonAnywhere Python Client"
        assert call.response.ok is True

    @responses.activate
    def test_make_request_not_okay(self, api_client):
        responses.add(responses.GET, self.get_url("console/"), status=404)

        with pytest.raises(PythonAnywhereError):
            api_client.console()


class TestConstructConsoles(PythonAnywhereTestCase):

    @responses.activate
    def test_consoles(self, api_client):
        url_path = "consoles/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles()
        self.asserts(url_path)

    @responses.activate
    def test_consoles_shared_with_you(self, api_client):
        url_path = "consoles/shared_with_you/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles.shared_with_you()
        self.asserts(url_path)

    @responses.activate
    def test_consoles_console_id(self, api_client):
        url_path = "consoles/123/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.consoles(console_id=123)
        self.asserts(url_path)

    @responses.activate
    def test_consoles_delete_console_id(self, api_client):
        url_path = "consoles/123/"
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.consoles.delete(console_id=123)
        self.asserts(url_path, "DELETE")


class TestConstructFiles(PythonAnywhereTestCase):

    @responses.activate
    def test_files_create(self, api_client):
        url_path = "files/sharing/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client.files.sharing.create(
            data={"path": "test/path"}
        )
        self.asserts(
            url_path,
            "POST",
            ["path=test%2Fpath"]
        )

    @responses.activate
    def test_files_sharing(self, api_client):
        url_path = "files/sharing/?path=test%2Fpath"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.files.sharing(path="test/path")
        self.asserts(url_path)

    @responses.activate
    def test_files_sharing_delete(self, api_client):
        url_path = "files/sharing/?path=test%2Fpath"
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.files.sharing.delete(path="test/path")
        self.asserts(url_path, "DELETE")

    @responses.activate
    def test_files_tree(self, api_client):
        url_path = "files/tree/?path=test%2Fpath"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.files.tree(path="test/path")
        self.asserts(url_path)


class TestConstructWebapps(PythonAnywhereTestCase):

    @responses.activate
    def test_webapps(self, api_client):
        url_path = "webapps/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps()
        self.asserts(url_path)

    @responses.activate
    def test_webapps_create(self, api_client):
        url_path = "webapps/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.create(data={
                "domain_name": "www.test.com",
                "python_version": "python27",
        })
        self.asserts(
            url_path,
            "POST",
            ["domain_name=www.test.com", "python_version=python27"]
        )

    @responses.activate
    def test_webapps_get_by_domain_name(self, api_client):
        url_path = "webapps/test.com/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps(domain_name="test.com")
        self.asserts(url_path)

    @responses.activate
    def test_webapps_update_by_domain_name(self, api_client):
        url_path = "webapps/test.com/"
        responses.add(responses.PUT, self.get_url(url_path))
        api_client.webapps.update(
            domain_name="test.com", data={"python_version": "python27"}
        )
        self.asserts(url_path, "PUT", ["python_version=python27"])

    @responses.activate
    def test_webapps_delete_by_domain_name(self, api_client):
        url_path = "webapps/test.com/"
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.webapps.delete(domain_name="test.com")
        self.asserts(url_path, "DELETE")

    @responses.activate
    def test_webapps_reload(self, api_client):
        url_path = "webapps/test.com/reload/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.reload(domain_name="test.com")
        self.asserts(url_path, "POST")


class TestConstructWebappsStaicFiles(PythonAnywhereTestCase):

    @responses.activate
    def test_webapps_static_files(self, api_client):
        url_path = "webapps/test.com/static_files/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps.static_files(
            domain_name="test.com"
        )
        self.asserts(url_path)

    @responses.activate
    def test_webapps_static_files_create(self, api_client):
        url_path = "webapps/test.com/static_files/"
        responses.add(responses.POST, self.get_url(url_path))
        api_client.webapps.static_files.create(
            domain_name="test.com", data={
                "url": "/static/",
                "path": "/test/path/"
            }
        )
        self.asserts(
            url_path, "POST", ["url=%2Fstatic%2F", "path=%2Ftest%2Fpath%2F"]
        )

    @responses.activate
    def test_webapps_static_files_get_by_static_id(self, api_client):
        url_path = "webapps/test.com/static_files/123/"
        responses.add(responses.GET, self.get_url(url_path))
        api_client.webapps.static_files(
            domain_name="test.com", static_id=123
        )
        self.asserts(url_path)

    @responses.activate
    def test_webapps_static_files_update_by_static_id(self, api_client):
        url_path = "webapps/test.com/static_files/123/"
        responses.add(responses.PUT, self.get_url(url_path))
        api_client.webapps.static_files.update(
            domain_name="test.com", static_id=123, data={
                "url": "/static/",
                "path": "/test/path/"
            }
        )
        self.asserts(
            url_path, "PUT", ["url=%2Fstatic%2F", "path=%2Ftest%2Fpath%2F"]
        )

    @responses.activate
    def test_webapps_static_files_delete_by_static_id(self, api_client):
        url_path = "webapps/test.com/static_files/123/"
        responses.add(responses.DELETE, self.get_url(url_path))
        api_client.webapps.static_files.delete(
            domain_name="test.com", static_id=123
        )
        self.asserts(url_path, "DELETE")
