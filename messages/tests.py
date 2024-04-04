from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_write_message_view(self):
        url = reverse('write_message')
        data = {'sender': 'user1', 'receiver': 'user2', 'message': 'Hello', 'subject': 'Test'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Message written successfully', response.content.decode())