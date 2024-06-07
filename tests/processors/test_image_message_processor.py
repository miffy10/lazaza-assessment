import os
import json
import unittest
from unittest.mock import Mock, patch
from http import HTTPStatus

from src.utilities.error_codes import FAILURE_ERROR_CODE, SUCCESS_ERROR_CODE
from src.processors.image_message_processor import ImageUpscaleMessageProcessor

class TestImageUpscaleClient(unittest.TestCase):

    def setUp(self):
        # Read the sample image file
        with open(os.path.join(os.path.dirname(__file__), 'test_input_image.json'), "r") as input_file:
            self.input_image = json.load(input_file)
        self.upscale_processor = ImageUpscaleMessageProcessor(self.input_image)

    def test_process_message_upscale_post_image_success(self):

         mock_validate_response = Mock(return_value=SUCCESS_ERROR_CODE)
         mock_upscale_response = Mock(return_value={'status_code': SUCCESS_ERROR_CODE, 'image': {'base64_image': self.input_image}})
         mock_post_response = Mock(return_value=Mock(status_code=HTTPStatus.OK))

         self.upscale_processor._validate_image_message = mock_validate_response
         self.upscale_processor.image_upscale_client.upscale_image = mock_upscale_response
         self.upscale_processor.image_service_client.post_image = mock_post_response

         result = self.upscale_processor.process_message()
         self.assertEqual(result, SUCCESS_ERROR_CODE)

    def test_process_message_failure_invalid_image(self):

        mock_validate_response = Mock(return_value=FAILURE_ERROR_CODE)
        self.upscale_processor._validate_image_message = mock_validate_response

        result = self.upscale_processor.process_message()

        self.assertEqual(result, FAILURE_ERROR_CODE)


    def test_process_message_upscale_failure(self):

        mock_validate_response = Mock(return_value=SUCCESS_ERROR_CODE)
        mock_upscale_response = Mock(return_value={'status_code': FAILURE_ERROR_CODE, 'image': None})


        self.upscale_processor._validate_image_message = mock_validate_response
        self.upscale_processor.image_upscale_client.upscale_image = mock_upscale_response

        result = self.upscale_processor.process_message()
        self.assertEqual(result, FAILURE_ERROR_CODE)


    def test_process_message_post_failure(self):

        mock_validate_response = Mock(return_value=SUCCESS_ERROR_CODE)
        mock_upscale_response = Mock(return_value={'status_code': SUCCESS_ERROR_CODE, 'image': {'base64_image': self.input_image}})
        mock_post_response = Mock(return_value=Mock(status_code=HTTPStatus.BAD_REQUEST))

        self.upscale_processor._validate_image_message = mock_validate_response
        self.upscale_processor.image_service_client.post_image = mock_upscale_response
        self.upscale_processor.image_service_client.post_image = mock_post_response

        result = self.upscale_processor.process_message()

        self.assertEqual(result, FAILURE_ERROR_CODE)


if __name__ == '__main__':
    unittest.main()
