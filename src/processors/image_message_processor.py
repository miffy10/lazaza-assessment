import abc
from http import HTTPStatus
import logging

from src.clients.image_service_client import ImageServiceClient
from src.clients.image_upscale_client import ImageUpscaleClient
from src.utilities.error_codes import FAILURE_ERROR_CODE, SUCCESS_ERROR_CODE

logging.basicConfig(level=logging.DEBUG)

class AbstractMessageProcessor(abc.ABC):
    @abc.abstractmethod
    def process_message(self) -> None:
        pass

class ImageUpscaleMessageProcessor(AbstractMessageProcessor):

    def __init__(self, image_message:dict):
        self.image_message = image_message
        self.image_service_client = ImageServiceClient()
        self.image_upscale_client = ImageUpscaleClient()

    def _validate_image_message(self) -> int:

        image_data = self.image_message.get('image_data', None)
        new_height = self.image_message.get('height', None)
        new_width = self.image_message.get('width', None)

        if not all((image_data, new_height, new_width)):
            return FAILURE_ERROR_CODE

        if not isinstance(new_height, int) or not isinstance(new_height, int):
            return FAILURE_ERROR_CODE

        return SUCCESS_ERROR_CODE

    def process_message(self) -> int:

        if self._validate_image_message() == FAILURE_ERROR_CODE:
            logging.error("Failed: Invalid image data.")
            return FAILURE_ERROR_CODE

        image_data, new_height, new_width = (self.image_message['image_data'], self.image_message['height'],
                                             self.image_message['width'])

        image_upscale = self.image_upscale_client.upscale_image(image_data, new_height, new_width)

        if image_upscale.get('status_code') == FAILURE_ERROR_CODE or not image_upscale.get('image',None):
            logging.error(f"Failed: Unable to upscale current image to height {new_height} and width {new_width}")
            return FAILURE_ERROR_CODE

        logging.info(f"Success: Upscaled current image to height {new_height} and width {new_width}.")

        upscaled_image = image_upscale.get('image').get('base64_image')
        image_post_status = self.image_service_client.post_image(upscaled_image)
        if image_post_status.status_code != HTTPStatus.OK:
                logging.error("Failed: Unable to upscale and post the image.")
                return FAILURE_ERROR_CODE

        logging.info("Success: Image posted.")
        return SUCCESS_ERROR_CODE