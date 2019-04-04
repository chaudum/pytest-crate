import random
import shutil
import string
import tempfile
from datetime import datetime
from typing import Callable, Generator

import pytest
from cr8.run_crate import CrateNode, get_crate
from crate.client import connect
from crate.client.cursor import Cursor

__all__ = ["crate"]


class CrateLayer:

    node: CrateNode
    crate_dir: str
    tmp: str

    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.crate_dir = get_crate(version)
        print(f"name={name} version={version}")

    def __repr__(self) -> str:
        return self.name

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._stop()

    def _start(self) -> None:
        print(f"Starting CrateDB {self} ...")
        self.tmp = tempfile.mkdtemp()
        settings = {
            "cluster.name": self.name,
            "path.data": self.tmp,
        }
        env = {"CRATE_HOME": self.crate_dir}
        self.node = CrateNode(
            crate_dir=self.crate_dir, keep_data=False, settings=settings, env=env
        )
        self.node.start()
        print(f"CrateDB {self} started")

    def _stop(self) -> None:
        print(f"Stopping CrateDB {self} ...")
        self.node.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)
        print(f"CrateDB {self} stopped")

    def dsn(self) -> str:
        return self.node.http_url


CrateLayerGenerator = Generator[CrateLayer, None, None]
CrateLayerFactory = Callable[[str, str], CrateLayerGenerator]
CrateLayerFactoryGenerator = Generator[CrateLayerFactory, None, None]


class CratePlugin:
    """
    Integrates CrateDB into pytest integration tests.
    """

    # noinspection SpellCheckingInspection
    @staticmethod
    def pytest_addoption(parser):
        """
        Adds custom options to the ``pytest`` command.
        https://docs.pytest.org/en/latest/writing_plugins.html#_pytest.hookspec.pytest_addoption
        """
        group = parser.getgroup("crate", "integration tests")
        group.addoption(
            "--crate-version",
            dest="crate_version",
            default="latest-stable",
            help="CrateDB version"
        )

    @pytest.fixture(scope="session")
    def crate_version(self, pytestconfig) -> Generator[str, None, None]:
        yield pytestconfig.getoption("crate_version")

    @pytest.fixture(scope="session")
    def crate_layer(self) -> CrateLayerFactoryGenerator:
        def layer_factory(name: str, version: str):
            with CrateLayer(name, version) as layer:
                yield layer
        yield layer_factory

    @pytest.fixture(scope="session")
    def crate(self, crate_layer, crate_version) -> CrateLayerGenerator:
        id = "".join(random.sample(string.ascii_letters, 8))
        date = datetime.utcnow().strftime("%Y%m%d%H%M")
        yield from crate_layer(f"pytest-crate-{date}-{id}", crate_version)

    @pytest.fixture
    def crate_cursor(self, crate) -> Generator[Cursor, None, None]:
        with connect(crate.dsn()) as connection:
            yield connection.cursor()

    @pytest.fixture
    def crate_execute(self, crate_cursor) -> Generator[Callable, None, None]:
        yield crate_cursor.execute


crate = CratePlugin()
