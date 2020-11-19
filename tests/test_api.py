# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import Mock, patch

from werkzeug.exceptions import BadRequest

from . import TEST_TOKEN


class ServitorTestCase(TestCase):
    auth_headers = {
        "Authorization": f"Bearer {TEST_TOKEN}"
    }

    def setUp(self):
        from servitor import app
        app.config['TESTING'] = True

        self.app = app
        self.client = app.test_client()


class TestAPI(ServitorTestCase):
    def test_root(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 404)

    @patch("servitor.Service.put")
    @patch("servitor.Service.get")
    def test_service(self, mock_get, mock_put):
        mock_get.return_value = {}
        mock_put.return_value = {}

        res = self.client.get('/service/some-swarm/some-service', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.client.get('/service/some-swarm/some-service',
                              headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_get.assert_called_with(
            env="some-swarm", name="some-service")

        res = self.client.put('/service/some-swarm/some-service', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.client.put('/service/some-swarm/some-service',
                              headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_put.assert_called_with(
            env="some-swarm", name="some-service")

    @patch("servitor.Stack.put")
    @patch("servitor.Stack.get")
    def test_stack(self, mock_get, mock_put):
        mock_get.return_value = {}
        mock_put.return_value = {}

        res = self.client.get('/stack/some-swarm/some-stack', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.client.get('/stack/some-swarm/some-stack',
                              headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_get.assert_called_with(env="some-swarm", name="some-stack")

        res = self.client.put('/stack/some-swarm/some-stack', headers={})
        self.assertEqual(res.status_code, 401)

        res = self.client.put('/stack/some-swarm/some-stack',
                              headers=self.auth_headers)
        self.assertEqual(res.status_code, 200)
        mock_put.assert_called_with(env="some-swarm", name="some-stack")


class TestResources(ServitorTestCase):
    def setUp(self):
        self.swarm = Mock()

        import servitor.resources
        servitor.resources.Swarm = Mock(return_value=self.swarm)

        super().setUp()

    def test_get_service(self):
        from servitor.resources import Service
        resource = Service()

        self.swarm.get_service_image.return_value = "some-image"
        res, code = resource.get(env="some-swarm", name="some-service")

        self.assertEqual(code, 200)
        self.assertEqual(res, "some-image")

    def test_put_service(self):
        from servitor.resources import Service
        resource = Service()

        with self.app.test_request_context('/'):
            with self.assertRaises(BadRequest):
                res, code = resource.put(env="some-swarm", name="some-ervice")

        mock_service = Mock()
        self.swarm.get_service.return_value = mock_service

        with self.app.test_request_context('/?image=some-image'):
            res, code = resource.put(env="some-swarm", name="some-service")

        self.assertEqual(code, 200)
        self.swarm.force_update.assert_called_with(mock_service, "some-image")

    def test_get_stack(self):
        from servitor.resources import Stack
        resource = Stack()

        services = [Mock(), Mock()]
        services[0].name = "service1"
        services[1].name = "service2"
        self.swarm.get_stack_services.return_value = services
        self.swarm.get_service_image.side_effect = ["image1", "image2"]
        res, code = resource.get(env="some-swarm", name="some-stack")

        self.assertEqual(code, 200)
        self.assertDictEqual(res, {"service1": "image1", "service2": "image2"})

    def test_put_stack(self):
        from servitor.resources import Stack
        resource = Stack()

        with self.app.test_request_context('/'):
            with self.assertRaises(BadRequest):
                res, code = resource.put(env="some-swarm", name="some-stack")

        with self.app.test_request_context('/?image=some-image'):
            with self.assertRaises(BadRequest):
                res, code = resource.put(env="some-swarm", name="some-stack")

        mock_service = Mock()
        self.swarm.get_stack_services.return_value = [mock_service]
        self.swarm.get_service_image.return_value = "some-other-image:latest"

        with self.app.test_request_context('/?image=some-image:stable'):
            with self.assertRaises(BadRequest):
                res, code = resource.put(env="some-swarm", name="some-stack")
        mock_service.update.assert_not_called()

        self.swarm.get_service_image.return_value = "some-image:latest"

        with self.app.test_request_context('/?image=some-image:stable'):
            res, code = resource.put(env="some-swarm", name="some-stack")

        self.assertEqual(code, 200)
        self.swarm.force_update.assert_called_with(mock_service,
                                                   "some-image:stable")
