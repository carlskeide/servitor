# -*- coding: utf-8 -*-
from . import TestCase, patch, TEST_TOKEN


class TestAPI(TestCase):
    def setUp(self):
        from servitor import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_root(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 404)

    @patch("servitor.Service.get")
    def test_service(self, mock_service):
        mock_service.return_value = {}
        res = self.client.get('/service/some-swarm/some-service',
                              query_string={"token": TEST_TOKEN})

        mock_service.assert_called_with(
            env="some-swarm", name="some-service")
        self.assertEqual(res.status_code, 200)

    @patch("servitor.Stack.get")
    def test_stack(self, mock_stack):
        mock_stack.return_value = {}
        res = self.client.get('/stack/some-swarm/some-stack',
                              query_string={"token": TEST_TOKEN})

        mock_stack.assert_called_with(env="some-swarm", name="some-stack")
        self.assertEqual(res.status_code, 200)
