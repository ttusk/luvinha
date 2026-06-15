import pytest
from glove import GloveModel


@pytest.fixture(scope="session")
def model():
    m = GloveModel()
    m.load()
    return m