# -*- coding: utf-8 -*-
from . import TestCase, patch, TEST_TOKEN


class TestAPI(TestCase):
    auth_headers = {
        "Authorization": f"Bearer {TEST_TOKEN}"
    }

    def setUp(self):
        from servitor import app
        app.config['TESTING'] = True

        client = app.test_client()
        self.get = client.get
        self.put = client.put

    def test_root(self):
        res = self.get('/')
        self.assertEqual(res.status_code, 404)

    @patch("servitor.Service.put")
    @patch("servitor.Service.get")
    def test_service(self, mock_get, mock_put):
        mock_get.return_value = {}
        mock_put.return_value = {}

        res = self.get('/service/some-swarm/some-service', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.get('/service/some-swarm/some-service',
                       headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_get.assert_called_with(
            env="some-swarm", name="some-service")

        res = self.put('/service/some-swarm/some-service', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.put('/service/some-swarm/some-service',
                       headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_put.assert_called_with(
            env="some-swarm", name="some-service")

    @patch("servitor.Stack.put")
    @patch("servitor.Stack.get")
    def test_stack(self, mock_get, mock_put):
        mock_get.return_value = {}
        mock_put.return_value = {}

        res = self.get('/stack/some-swarm/some-stack', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.get('/stack/some-swarm/some-stack',
                       headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_get.assert_called_with(env="some-swarm", name="some-stack")

        res = self.put('/stack/some-swarm/some-stack', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.put('/stack/some-swarm/some-stack',
                       headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_put.assert_called_with(env="some-swarm", name="some-stack")
