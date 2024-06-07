import os
import json
import unittest
from unittest.mock import Mock, patch
import urllib.error

from src.utilities.error_codes import FAILURE_ERROR_CODE, SUCCESS_ERROR_CODE
from src.clients.image_upscale_client import ImageUpscaleClient

class TestImageUpscaleClient(unittest.TestCase):

    def setUp(self):
        # Read the sample image file
        self.upscale_client = ImageUpscaleClient()
        with open(os.path.join(os.path.dirname(__file__), 'test_input_image.json'), "r") as input_file:
            self.input_image = json.load(input_file)

    @patch("src.clients.image_upscale_client.urllib.request.urlopen")
    def test_upscale_image_success(self,mock_urlopen):

        urllib_mock_response = Mock()
        urllib_mock_response.read.return_value = json.dumps({'base64_image': self.input_image}).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = urllib_mock_response

        result = self.upscale_client.upscale_image(self.input_image,500,
                                     700)
        self.assertEqual(result['status_code'], SUCCESS_ERROR_CODE)
        self.assertIsNotNone(result['image'])

    @patch("src.clients.image_upscale_client.urllib.request.urlopen")
    def test_upscale_image_failure_invalid_input(self,mock_urlopen):
        mock_error = urllib.error.HTTPError(
            url='mock_url',
            code=400,
            msg='Bad request',
            hdrs=None,
            fp=None
        )
        mock_error.read = Mock(return_value=json.dumps({"message": "new_width or new_height are invalid"}).encode('utf-8'))
        mock_urlopen.side_effect = mock_error

        result = self.upscale_client.upscale_image(self.input_image, 100, 100)
        self.assertEqual(result['status_code'], FAILURE_ERROR_CODE)
        self.assertIsNone(result['image'])

    @patch("src.clients.image_upscale_client.urllib.request.urlopen")
    def test_upscale_image_failure_service_unavailable(self,mock_urlopen):

        mock_error = urllib.error.HTTPError(
            url='mock_url',
            code=500,
            msg='Internal Server Error',
            hdrs=None,
            fp=None
        )
        mock_error.read = Mock(
            return_value=json.dumps({"message": "Error resizing image.  Sorry, you can't count on a service being available all the time..."}).encode('utf-8'))
        mock_urlopen.side_effect = mock_error

        result = self.upscale_client.upscale_image(self.input_image, 100, 100)
        self.assertEqual(result['status_code'], FAILURE_ERROR_CODE)
        self.assertIsNone(result['image'])

    @patch("src.clients.image_upscale_client.urllib.request.urlopen")
    def test_upscale_image_failure_invalid_access_token(self,mock_urlopen):
        mock_error = urllib.error.HTTPError(
            url='mock_url',
            code=401,
            msg='Unauthorized',
            hdrs=None,
            fp=None
        )
        mock_error.read = Mock(
            return_value=json.dumps({"message": "Invalid access_token"}).encode('utf-8'))
        mock_urlopen.side_effect = mock_error

        result = self.upscale_client.upscale_image(self.input_image, 100, 100)
        self.assertEqual(result['status_code'], FAILURE_ERROR_CODE)
        self.assertIsNone(result['image'])

if __name__ == '__main__':
    unittest.main()
