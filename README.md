# Warrant Python Library

Use [Warrant](https://warrant.dev/) in Python projects.

[![PyPI](https://img.shields.io/pypi/v/warrant-python)](https://pypi.org/project/warrant-python/)
[![Slack](https://img.shields.io/badge/slack-join-brightgreen)](https://join.slack.com/t/warrantcommunity/shared_invite/zt-12g84updv-5l1pktJf2bI5WIKN4_~f4w)

## Installation

```python
pip install warrant-python
```

## Usage

```python
import warrant

warrant.api_key = "api_test_f5dsKVeYnVSLHGje44zAygqgqXiLJBICbFzCiAg1E="

warrant.User.create()
warrant.Tenant.create(id="dunder_mifflin")
```

## Configuring the API Endpoint
---
The API endpoint the SDK makes requests to is configurable via the `warrant.api_endpoint` attribute:

```python
import warrant

# Set api endpoint to http://localhost:8000
warrant.api_endpoint = 'http://localhost:8000'
```

We’ve used a random API key in these code examples. Replace it with your
[actual publishable API keys](https://app.warrant.dev) to
test this code through your own Warrant account.

For more information on how to use the Warrant API, please refer to the
[Warrant API reference](https://docs.warrant.dev).

Note that we may release new [minor and patch](https://semver.org/) versions of this library with small but backwards-incompatible fixes to the type declarations. These changes will not affect Warrant itself.

## Warrant Documentation

- [Warrant Docs](https://docs.warrant.dev/)
