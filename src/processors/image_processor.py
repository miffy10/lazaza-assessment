import abc
import logging

from src.clients.queue_client import QueueClient
from src.clients.image_service_client import ImageServiceClient
from src.clients.image_upscale_client import ImageUpscaleClient

logging.basicConfig(level=logging.DEBUG)


class AbstractImageProcessor(abc.ABC):
    @abc.abstractmethod
    def process_image(self):
        pass


class ImageUpscaleProcessor(AbstractImageProcessor):

    def __init__(self, queue_client: QueueClient, image_service_client: ImageServiceClient,
                 image_upscale_client: ImageUpscaleClient):
        self.queue_client = queue_client
        self.image_service_client = image_service_client
        self.image_upscale_client = image_upscale_client

    def process_image(self):
        while True:
            image_message = self.queue_client.pop()
            if not image_message:
                break
            logging.info("Upscaling next image in the Queue")
            self.process_single_image(image_message)

        logging.info("Attempted to upscale all images in the queue. Queue is now empty.")

    def process_single_image(self, image_message) -> None:
        image_data = image_message.get('image_data', None)
        new_height = image_message.get('height', None)
        new_width = image_message.get('width', None)

        if not all((image_data, new_height, new_width)):
            logging.error("Failed: Invalid image data.")
            return

        try:
            new_height, new_width = int(new_height), int(new_width)
        except (ValueError, TypeError) as e:
            logging.error(f"Failed: Unable to upscale current image. \n Reason: {e}")
            return

        upscale_status = self.image_upscale_client.upscale_image(image_data, new_height, new_width)

        if not upscale_status:
            logging.info(f"Success: Upscaled current image to height {new_height} and width {new_width}.")
            post_image_status = self.image_service_client.post_image(image_data)
            if post_image_status.status_code == 200:
                logging.info("Success: Image posted.")
            else:
                logging.info("Failed: Unable to upscale and post the image.")
        else:
            logging.error(f"Failed: Unable to upscale current image to height {new_height} and width {new_width}")
