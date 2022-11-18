import pytest
from pytest_django.lazy_django import skip_if_no_django
from pytest_django.fixtures import SettingsWrapper
from typing import Generator

pytestmark = [pytest.mark.django_db]


@pytest.fixture(scope="session")
def session_settings() -> "Generator":
    skip_if_no_django()
    wrapper = SettingsWrapper()
    yield wrapper
    wrapper.finalize()
