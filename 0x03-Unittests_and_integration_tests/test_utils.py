#!/usr/bin/env python3
"""
Unit tests for utils.py module.
Covers access_nested_map, get_json, and memoize decorator.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function in utils."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the correct value."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function in utils."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected JSON response."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        self.assertEqual(utils.get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            """Inner test class with memoized property."""

            def a_method(self):
                """Return a constant value."""
                return 42

            @utils.memoize
            def a_property(self):
                """Return result of a_method, memoized."""
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock_method:
            mock_method.return_value = 42
            obj = TestClass()

            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()
