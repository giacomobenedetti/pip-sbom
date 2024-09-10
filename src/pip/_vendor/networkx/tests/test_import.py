import pytest


def test_namespace_alias():
    with pytest.raises(ImportError):
        from pip._vendor.networkx import nx


def test_namespace_nesting():
    with pytest.raises(ImportError):
        from pip._vendor.networkx import networkx
