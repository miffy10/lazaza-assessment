from src.clients.queue_client import QueueClient
from src.clients.image_service_client import ImageServiceClient
from src.clients.image_upscale_client import ImageUpscaleClient
from src.processors.image_processor import ImageUpscaleProcessor

def main():
    # Instantiate clients and processor
    queue_client = QueueClient()
    image_service_client = ImageServiceClient()
    image_upscale_client = ImageUpscaleClient()
    image_processor = ImageUpscaleProcessor(queue_client,image_service_client, image_upscale_client)

    # Process images
    image_processor.process_image()
if __name__ == "__main__":
    main()