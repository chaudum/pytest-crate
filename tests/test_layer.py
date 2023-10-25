import pytest
from crate.client import connect


@pytest.fixture(scope="session")
def custom_crate_a(crate_layer):
    yield from crate_layer("crate_a", "5.4.x")


@pytest.fixture(scope="session")
def custom_crate_b(crate_layer, crate_version):
    settings = {
        "node.name": "custom-node-name",
    }
    yield from crate_layer("crate_b", crate_version, **settings)


def test_crate(crate):
    assert crate.dsn().startswith("http://127.0.0.1:42")
    assert "http" in crate.addresses
    assert crate.addresses["http"].host == "127.0.0.1"
    assert 4300 > crate.addresses["http"].port >= 4200
    assert "psql" in crate.addresses
    assert crate.addresses["psql"].host == "127.0.0.1"
    assert 5500 > crate.addresses["psql"].port >= 5432
    assert "transport" in crate.addresses
    assert crate.addresses["transport"].host == "127.0.0.1"
    assert 4400 > crate.addresses["transport"].port >= 4300


def test_cursor(crate_cursor):
    crate_cursor.execute("SELECT 1")
    assert crate_cursor.fetchone() == [1]


def test_execute(crate_execute, crate_cursor):
    for stmt in [
        "CREATE TABLE pytest (name STRING, version INT)",
        "INSERT INTO pytest (name, version) VALUES ('test_execute', 1)",
        "REFRESH TABLE pytest",
    ]:
        crate_execute(stmt)
    crate_cursor.execute("SELECT name, version FROM pytest")
    assert crate_cursor.fetchall() == [["test_execute", 1]]


def test_custom_crates(custom_crate_a, custom_crate_b):
    assert custom_crate_a.name == "crate_a"
    assert custom_crate_b.name == "crate_b"


def test_crate_with_custom_settings(custom_crate_b):
    assert custom_crate_b.name == "crate_b"
    assert custom_crate_b.settings == {
        "node.name": "custom-node-name",
    }
    with connect(custom_crate_b.dsn()) as conn:
        cursor = conn.cursor()
        for stmt, expected in [
                ["SELECT name FROM sys.cluster", ["crate_b"]],
                ["SELECT name FROM sys.nodes", ["custom-node-name"]],
        ]:
            cursor.execute(stmt)
            assert cursor.fetchone() == expected
