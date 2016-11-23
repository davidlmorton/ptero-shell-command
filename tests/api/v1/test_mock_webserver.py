from .base import BaseAPITest


class TestMockWebserver(BaseAPITest):
    def test_mock_webserver_works(self):
        webhook_target = self.create_webhook_server([302])
        import requests
        request_body = {"bob": "hi im your friend"}
        response = requests.post(webhook_target.url, json=request_body)
        self.assertEqual(302, response.status_code)

        history = webhook_target.stop()
        self.assertEqual(request_body, history[0]['data'])
