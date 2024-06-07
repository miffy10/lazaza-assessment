import abc
import json
from http import HTTPStatus
import logging
import ssl
import urllib.request
import urllib.error

from src.utilities.error_codes import FAILURE_ERROR_CODE, SUCCESS_ERROR_CODE
# Access token should not be exposed in code and have hidden in temporary config file
from src.utilities.image_upscale_config import IMAGE_UPSCALE_URL, ACCESS_TOKEN

logging.basicConfig(level=logging.DEBUG)
# Disable SSL certificate verification
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_NONE

class AbstractImageUpscaleClient(abc.ABC):
    @abc.abstractmethod
    def upscale_image(self, image: bytes, new_height: int, new_width: int) -> dict:
        pass

class ImageUpscaleClient(AbstractImageUpscaleClient):

    def __init__(self):
        self.image_upscale_url = IMAGE_UPSCALE_URL
        self.__access_token = ACCESS_TOKEN

    def upscale_image(self, image: bytes, new_height: int, new_width: int):

        HTTP_HEADER = {'Content-Type': 'application/json'}
        request_body = {
            'access_token': self.__access_token,
            'new_height': new_height,
            'new_width': new_width,
            'base64_image': image
        }

        request_data = json.dumps(request_body).encode('utf-8')
        request = urllib.request.Request(self.image_upscale_url, data=request_data, headers=HTTP_HEADER, method='POST')

        try:
            with urllib.request.urlopen(request, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                return {'image': json.loads(response_data), 'status_code': SUCCESS_ERROR_CODE}
        except urllib.error.HTTPError as err:
            logging.error(f"{HTTPStatus(err.code).phrase}: {err.read().decode('utf-8')}")
        except urllib.error.URLError as err:
            logging.error(f"Image Upscale Service Error: {err}")

        return {'image': None, 'status_code': FAILURE_ERROR_CODE}

