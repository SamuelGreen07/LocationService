import aiohttp
from geopy.distance import geodesic
from location.services.location_integrations.base import BaseLocationService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NominatimLocationService(BaseLocationService):

    async def get_address(self, latitude, longitude):
        logger.info(f"Fetching address for coordinates: ({latitude}, {longitude})")
        timeout = aiohttp.ClientTimeout(total=1000)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            logger.info(f"Created aiohttp.ClientSession for coordinates: ({latitude}, {longitude})")
            async with client.get('https://nominatim.openstreetmap.org/reverse', params={
                'format': 'json',
                'lat': latitude,
                'lon': longitude
            }) as response:
                logger.info(f"Received response with status: {response.status} for coordinates: ({latitude}, {longitude})")
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Received data: {data}")
                    return data.get('display_name', '')
                return ''


    def get_distance(self, point1, point2):
        return geodesic(point1, point2).meters


nominatim_location_service = NominatimLocationService()
