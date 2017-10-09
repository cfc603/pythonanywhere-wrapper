import pytest

from pythonanywhere.client import PythonAnywhere


@pytest.fixture(scope="session")
def api_client():
    """Returns PythonAnywhere instance"""
    return PythonAnywhere("api_key", user="testuser")
