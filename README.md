# Warrant Python Library

Use [Warrant](https://warrant.dev/) in Python projects.

[![PyPI](https://img.shields.io/pypi/v/warrant-python)](https://pypi.org/project/warrant-python/)
[![Discord](https://img.shields.io/discord/865661082203193365?label=discord)](https://discord.gg/QNCMKWzqET)

## Installation

```python
pip install warrant-python
```

## Usage

```python
import warrant

warrant = Warrant("api_test_f5dsKVeYnVSLHGje44zAygqgqXiLJBICbFzCiAg1E=")
warrant.create_user()
```

We’ve used a random API key in these code examples. Replace it with your
[actual publishable API keys](https://app.warrant.dev) to
test this code through your own Warrant account.

For more information on how to use the Warrant API, please refer to the
[Warrant API reference](https://docs.warrant.dev).

Note that we may release new [minor and patch](https://semver.org/) versions of this library with small but backwards-incompatible fixes to the type declarations. These changes will not affect Warrant itself.

## Warrant Documentation

- [Warrant Docs](https://docs.warrant.dev/)