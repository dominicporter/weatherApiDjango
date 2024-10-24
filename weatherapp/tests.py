from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class HelloWorldTests(APITestCase):
    def test_hello_world(self):
        """
        Ensure the /api/hello/ endpoint returns the expected message.
        """
        # Use the reverse() method to resolve the URL
        url = reverse('hello_world')  # This uses the URL name defined in urls.py

        # Make a GET request to the API endpoint
        response = self.client.get(url)

        # Check that the response status is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the message in the response matches what we expect
        self.assertEqual(response.data, {"message": "Hello, world!"})
