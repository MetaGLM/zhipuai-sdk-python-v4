"""Configuration for unit tests."""

from importlib import util
from pathlib import Path
from typing import Dict, Sequence

import pytest
from pytest import Config, Function, Parser

from zhipuai.core.logs import (
	get_config_dict,
	get_log_file,
	get_timestamp_ms,
)


def pytest_addoption(parser: Parser) -> None:
	"""Add custom command line options to pytest."""
	parser.addoption(
		'--only-extended',
		action='store_true',
		help='Only run extended tests. Does not allow skipping any extended tests.',
	)
	parser.addoption(
		'--only-core',
		action='store_true',
		help='Only run core tests. Never runs any extended tests.',
	)


def pytest_collection_modifyitems(config: Config, items: Sequence[Function]) -> None:
	"""Add implementations for handling custom markers.

	At the moment, this adds support for a custom `requires` marker.

	The `requires` marker is used to denote tests that require one or more packages
	to be installed to run. If the package is not installed, the test is skipped.

	The `requires` marker syntax is:

	.. code-block:: python

	    @pytest.mark.requires('package1', 'package2')
	    def test_something(): ...
	"""
	# Mapping from the name of a package to whether it is installed or not.
	# Used to avoid repeated calls to `util.find_spec`
	required_pkgs_info: Dict[str, bool] = {}

	only_extended = config.getoption('--only-extended') or False
	only_core = config.getoption('--only-core') or False

	if only_extended and only_core:
		raise ValueError('Cannot specify both `--only-extended` and `--only-core`.')

	for item in items:
		requires_marker = item.get_closest_marker('requires')
		if requires_marker is not None:
			if only_core:
				item.add_marker(pytest.mark.skip(reason='Skipping not a core test.'))
				continue

			# Iterate through the list of required packages
			required_pkgs = requires_marker.args
			for pkg in required_pkgs:
				# If we haven't yet checked whether the pkg is installed
				# let's check it and store the result.
				if pkg not in required_pkgs_info:
					try:
						installed = util.find_spec(pkg) is not None
					except Exception:
						installed = False
					required_pkgs_info[pkg] = installed

				if not required_pkgs_info[pkg]:
					if only_extended:
						pytest.fail(
							f'Package `{pkg}` is not installed but is required for '
							f'extended tests. Please install the given package and '
							f'try again.',
						)

					else:
						# If the package is not installed, we immediately break
						# and mark the test as skipped.
						item.add_marker(pytest.mark.skip(reason=f'Requires pkg: `{pkg}`'))
						break
		else:
			if only_extended:
				item.add_marker(pytest.mark.skip(reason='Skipping not an extended test.'))


@pytest.fixture
def logging_conf() -> dict:
	return get_config_dict(
		'info',
		get_log_file(log_path='logs', sub_dir=f'local_{get_timestamp_ms()}'),
		1024 * 1024,
		1024 * 1024 * 1024,
	)


@pytest.fixture
def test_file_path(request) -> Path:
	from pathlib import Path

	# 当前执行目录
	# 获取当前测试文件的路径
	test_file_path = Path(str(request.fspath)).parent
	print('test_file_path:', test_file_path)
	return test_file_path
