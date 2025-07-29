# ALX Backend Python: Unit and Integration Tests

This project contains unit and integration tests for Python modules in the ALX Backend curriculum. The tests focus on validating utilities and a GitHub client using common testing patterns like mocking, parameterization, and fixtures.

## Learning Objectives

- Understand the difference between unit and integration tests.
- Practice common testing techniques such as:
  - Mocking external dependencies.
  - Using parameterized tests for multiple input scenarios.
  - Applying fixtures for reusable test data.
- Write clean, documented, and type-annotated Python test code.

## Project Structure

- `utils.py` — Utility functions such as `access_nested_map`, `get_json`, and `memoize`.
- `client.py` — `GithubOrgClient` class for interacting with GitHub APIs.
- `fixtures.py` — Test fixtures containing sample payloads for integration tests.
- `test_utils.py` — Unit tests for utilities with parameterized cases.
- `test_client.py` — Unit and integration tests for the GitHub client.

## How to Run Tests

Ensure you have Python 3.7+ and `unittest` installed. Install dependencies if necessary:

```bash
pip install parameterized
```
