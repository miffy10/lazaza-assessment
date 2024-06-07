"""
Note : The solution implements a synchronous approach to reading from the queue and upscaling the images, considering that
Python is single-threaded. If there is a delay in the completion of the image upscaling API, all subsequent image processing
messages will also be delayed."

In future implementations, this can be improvised to an asynchronous approach, utilizing multithreading,
or employing multiprocessing. This can be achieved using the asyncio module or any other third-party module.
"""
from src.processors.queue_processor import QueueProcessor

def main():

    # Assuming all messages in the queue will be image upscale type.
    IMAGE_UPSCALE_REQUEST = 'IMAGE_UPSCALE'
    image_processor = QueueProcessor(IMAGE_UPSCALE_REQUEST)
    image_processor.process_queue()

if __name__ == "__main__":
    main()