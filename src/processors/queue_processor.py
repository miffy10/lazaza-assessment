"""
Note : This module  of code involves a network call, specifically making a call to an image upscaling API. When using a while True loop in a single-threaded Python program, it becomes synchronous, meaning the entire loop is blocked until each operation completes. In future implementations, this issue could be addressed by employing an asynchronous approach, utilizing multithreading, or implementing multiprocessing.
"""
import abc
import logging

from src.clients.queue_client import QueueClient
from src.processors.image_message_processor import ImageUpscaleMessageProcessor
from src.utilities.error_codes import FAILURE_ERROR_CODE, SUCCESS_ERROR_CODE

IMAGE_UPSCALE_REQUEST ='IMAGE_UPSCALE'

logging.basicConfig(level=logging.DEBUG)

class AbstractQueueProcessor(abc.ABC):
    @abc.abstractmethod
    def process_queue(self):
        pass

class QueueProcessor(AbstractQueueProcessor):

    def __init__(self, request_type=IMAGE_UPSCALE_REQUEST):
        self.queue_client = QueueClient()
        self.request_type = request_type

    def process_queue(self):
        if self.request_type != IMAGE_UPSCALE_REQUEST:
            logging.error('Unknown request type')
            return FAILURE_ERROR_CODE

        """
        This block of code involves a network call, specifically making a call to an image upscaling API. 
        When using a while True loop in a single-threaded Python program, it becomes synchronous, meaning the entire loop
        is blocked until each operation completes. In future implementations, this issue could be addressed by employing
        an asynchronous approach, utilizing multithreading, or multiprocessing using asyncio module or
        any other third-party module.
        """

        while True:
            image_message = self.queue_client.pop()
            if not image_message:
                break
            logging.info("****Processing next message in the Queue****")
            image_message_processor = ImageUpscaleMessageProcessor(image_message)
            image_process_status = image_message_processor.process_message()
            if image_process_status == FAILURE_ERROR_CODE:
                logging.error("Failed processing current message")
            else:
                logging.info("Success processing current message")

        logging.info("Attempted to process all messages in the queue. Queue is now empty.")
        return SUCCESS_ERROR_CODE