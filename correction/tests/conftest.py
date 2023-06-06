from os import path

import pytest
from lxml import etree


@pytest.fixture
def test_dir(request):
    return request.fspath.dirname


@pytest.fixture
def example(test_dir):
    fn = path.join(test_dir, 'laura23_0161.xml')
    return etree.parse(fn)
