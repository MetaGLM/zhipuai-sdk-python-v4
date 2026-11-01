# Installed-package smoke tests

Run these checks in a fresh environment after building and installing the wheel,
without installing test or development extras. This catches runtime dependencies
that an existing development environment can accidentally provide.

```sh
python -m pip wheel . --no-deps --wheel-dir dist
python -m venv /tmp/zhipuai-install-test
/tmp/zhipuai-install-test/bin/python -m pip install dist/zhipuai-*.whl
/tmp/zhipuai-install-test/bin/python -I tests/installation/test_installed_sdk.py -v
```

The isolated interpreter imports the installed package rather than the source
checkout. The tests create no API requests and require only runtime dependencies.
