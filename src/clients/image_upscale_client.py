import abc
import logging
import json
import urllib.request
import urllib.error
import ssl

logging.basicConfig(level=logging.DEBUG)

class AbstractImageUpscaleClient(abc.ABC):
    @abc.abstractmethod
    def upscale_image(self, image: bytes, new_height: int, new_width: int) -> int:
        pass

class ImageUpscaleClient(AbstractImageUpscaleClient):
    IMAGE_UPSCALE_URL = 'https://lazazaai00imgageresizer00.azurewebsites.net/api/upscale'
    ACCESS_TOKEN = "sukanya_thapa"
    HTTP_HEADER = {'Content-Type': 'application/json'}

    def _send_upscale_request(self, request_body: dict) -> dict:
        request_data = json.dumps(request_body).encode('utf-8')
        request = urllib.request.Request(self.IMAGE_UPSCALE_URL, data=request_data, headers=self.HTTP_HEADER, method='POST')

        # Disable SSL certificate verification
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ssl_context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(request, context=ssl_context) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data)

    def upscale_image(self, image: bytes, new_height: int, new_width: int) -> int:
        request_body = {
            'access_token': self.ACCESS_TOKEN,
            'new_height': new_height,
            'new_width': new_width,
            'base64_image': image
        }
        try:
            self._send_upscale_request(request_body)
            return 0
        except urllib.error.HTTPError as err:
            if err.code == 400:
                logging.error(f"Invalid input: {err.read().decode('utf-8')}")
            elif err.code == 500:
                logging.error(f"Service unavailable: {err.read().decode('utf-8')}")
            else:
                logging.error(f"HTTP Error: {err.read().decode('utf-8')}")
        except urllib.error.URLError as err:
            logging.error(f"Image Upscale Service Error: {err}")
        return 1