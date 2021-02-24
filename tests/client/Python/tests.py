# coding=utf-8
from __future__ import unicode_literals
from client import JudgeServerClient, JudgeServerClientError
import os
import json
import unittest
import requests


class JudgeServerClientForTokenHeaderTest(JudgeServerClient):
    def _request(self, url, data=None):
        kwargs = {"headers": {"Content-Type": "application/json"}}
        if data:
            kwargs["data"] = json.dumps(data)
        try:
            return requests.post(url, **kwargs).json()
        except Exception as e:
            raise JudgeServerClientError(e.message)


class JudgeServerTest(unittest.TestCase):
    def setUp(self):
        self.token = os.environ["TOKEN"]
        self.server_base_url = "http://127.0.0.1:" + os.environ["SERVICE_PORT"]
        self.client = JudgeServerClient(
            token=self.token, server_base_url=self.server_base_url)

    def test_success(self):
        data = self.client.ping()
        self.assertEqual(data["err"], None)
        self.assertEqual(data["data"]["action"], "pong")

    def test_invalid_token(self):
        client = JudgeServerClient(
            token="wrong token", server_base_url=self.server_base_url)
        data = client.ping()
        self.assertEqual(data["err"], "TokenVerificationFailed")

    def test_no_token_header(self):
        client = JudgeServerClientForTokenHeaderTest(
            token="wrong token", server_base_url=self.server_base_url)
        data = client.ping()
        self.assertEqual(data["err"], "TokenVerificationFailed")


if __name__ == '__main__':
    unittest.main()
