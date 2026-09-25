from config.bootstrap import Bootstrap, EnvConfig
from config.pytest_hooks import on_start, on_end, on_report


def pytest_configure(config):
    env = EnvConfig.from_conftest(__file__)
    Bootstrap(env).run()


def pytest_runtest_setup(item):
    on_start(item)


def pytest_runtest_teardown(item):
    on_end(item)


def pytest_runtest_makereport(item, call):
    on_report(item, call)