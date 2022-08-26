import unittest

import requests
from lru import *
from os import environ
from unittest import mock
from requests.exceptions import Timeout
from http import HTTPStatus


class TestOxfordCase(unittest.TestCase):
    def setUp(self) -> None:
        self.o = OxfordDictionary()
        self.env_vars = {"APP_ID": "blabla", "APP_KEY": "blabla"}

    def test_APP_not_set(self):

        for v in self.env_vars:
            with self.subTest(v=v):
                with self.assertRaises(KeyError):
                    environ[v]

    def test_APP_set(self):

        with mock.patch.dict(environ, self.env_vars):
            for v in self.env_vars:
                with self.subTest(v=v):
                    self.assertEqual(environ[v],"blabla")

    @mock.patch("lru.requests")
    def test_oxford_request_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        #
        with mock.patch.dict(environ, self.env_vars):
            with self.assertRaises(Timeout):
                self.o.search("test")
                mock_requests.get.assert_called_once()

    @mock.patch("lru.requests")
    def test_oxford_request_not_found(self, mock_requests):
        mock_requests.get.status_code = HTTPStatus.NOT_FOUND
        #
        with mock.patch.dict(environ, self.env_vars):
            with self.assertRaises(KeyError):
                self.o.search("test")
                mock_requests.get.assert_called_once()


    @mock.patch("lru.requests")
    def test_oxford_request_found(self, mock_requests):
        mock_requests.get.status_code = HTTPStatus.OK
        #
        with mock.patch.dict(environ, self.env_vars):
            with self.assertRaises(KeyError):
                self.o.search("test")
            mock_requests.get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
