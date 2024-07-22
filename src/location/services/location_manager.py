import io
import pandas as pd
from sqlalchemy import select
from limits import RateLimitItemPerSecond
import asyncio
import aiohttp
import logging

from app import db
from location.constants import TaskStatus
from location.models import Task, Point
from location.services.location_integrations.nominatim_service import nominatim_location_service
from services.limiter_service import limiter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocationServiceManager:
    LOCATION_INTEGRATIONS = {
        'nominatim': nominatim_location_service
    }

    def __init__(self, max_requests_per_second: int = 10):
        self.rate_limit = RateLimitItemPerSecond(max_requests_per_second)

    async def process_task(self, task_id, file_content):
        logger.info(f"Starting task {task_id}")
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            points = await self._process_points(task_id, df)
            links = self._calculate_distances(points)
            await self._finalize_task(task_id, points, links)
            logger.info(f"Task {task_id} completed successfully")
        except Exception as e:
            logger.error(f"Task {task_id} failed with error: {e}")

    async def _process_points(self, task_id, df):
        points = []
        async with db.get_session() as session:
            async with session.begin():
                for index, row in df.iterrows():
                    await self._acquire()
                    logger.info(f"Processing point {row['Point']} at ({row['Latitude']}, {row['Longitude']})")
                    address = await self._fetch_address(row['Latitude'], row['Longitude'])
                    point = Point(
                        name=row['Point'],
                        address=address,
                        latitude=row['Latitude'],
                        longitude=row['Longitude'],
                        task_id=task_id
                    )
                    session.add(point)
                    points.append({
                        'name': row['Point'],
                        'address': address,
                        'latitude': row['Latitude'],
                        'longitude': row['Longitude']
                    })
                await session.commit()
        return points

    def _calculate_distances(self, points):
        links = []
        total_distance = 0
        logger.info("Calculating distances between points")

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = self._calculate_distance(
                    (points[i]['latitude'], points[i]['longitude']),
                    (points[j]['latitude'], points[j]['longitude'])
                )
                total_distance += distance
                links.append({
                    'name': f'{points[i]["name"]} -->> {points[j]["name"]}',
                    'distance': round(distance, 2)
                })

        links.append({
            'name': "Total",
            'distance': round(total_distance, 2)
        })

        logger.info(f"Total distance calculated: {total_distance} meters")
        return links

    def _calculate_distance(self, point1, point2):
        from geopy.distance import geodesic
        return geodesic(point1, point2).meters

    async def _finalize_task(self, task_id, points, links):
        async with db.get_session() as session:
            async with session.begin():
                task = await session.get(Task, task_id)
                task.status = TaskStatus.FINISHED.value
                task.data = {
                    'points': points,
                    'links': links
                }
                await session.commit()
        logger.info(f"Task {task_id} finalized and saved to database")

    async def _acquire(self):
        return
        while True:
            if await limiter.hit(self.rate_limit):
                return
            logger.info("Rate limit hit, sleeping for 1 second")
            await asyncio.sleep(1)

    async def _fetch_address(self, latitude, longitude):
        for service_name, service in self.LOCATION_INTEGRATIONS.items():
            try:
                address = await service.get_address(latitude, longitude)
                logger.info(f"Fetched address from {service_name} for ({latitude}, {longitude}): {address}")
                return address
            except Exception as e:
                logger.error(f"Service {service_name} failed with error: {e}")
                continue
        raise Exception("All location services failed")

    async def get_task(self, task_id):
        async with db.get_session() as session:
            query = select(Task).where(Task.id == task_id)
            result = await session.execute(query)
            task = result.scalars().first()
        return task

location_service_manager = LocationServiceManager()
