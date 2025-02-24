import asyncio
import aiohttp
import logging
from collections import OrderedDict
from flask import current_app as app

from .consts import CACHE_SIZE

logger = logging.getLogger(__name__)

unstructured = None


class UnstructuredRequestSession:
    def __init__(self, unstructured_base_url, api_key):
        self.get_content_url = f"{unstructured_base_url}/general/v0/general"
        self.headers = {"unstructured-api-key": api_key}
        # Manually cache because functools.lru_cache does not support async methods
        self.cache = OrderedDict()
        self.start_session()

    def start_session(self):
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    def close_loop(self):
        self.loop.stop()
        self.loop.close()

    def cache_get(self, key):
        self.cache.move_to_end(key)

        return self.cache[key]

    def cache_put(self, key, item):
        self.cache[key] = item

        if len(self.cache) > CACHE_SIZE:
            self.cache.popitem()

    async def close_session(self):
        await self.session.close()

    async def get_unstructured_content(self, file):
        # Unpack tuple
        file_id, file_name, file_data = file

        # Check cache
        if file_id in self.cache:
            return self.cache_get(file_id)

        # Use FormData to pass in files parameter
        data = aiohttp.FormData()
        data.add_field("files", file_data, filename=file_name)

        async with self.session.post(
            self.get_content_url,
            headers=self.headers,
            data=data,
        ) as response:
            content = await response.json()
            if not response.ok:
                logger.error(f"Error response from Unstructured: {content}")
                return None

            self.cache_put(file_id, (file_name, content))

            return self.cache[file_id]

    async def gather(self, files):
        tasks = [self.get_unstructured_content(file) for file in files]
        return await asyncio.gather(*tasks)

    def batch_get(self, files):
        results = self.loop.run_until_complete(self.gather(files))
        results = [result for result in results if result is not None]

        result_dict = {
            filename: content[:20]
            for filename, content in results
            if content is not None
        }

        # Close session and loop
        self.loop.run_until_complete(self.close_session())
        self.close_loop()

        return result_dict


def get_unstructured_client():
    global unstructured
    if unstructured is not None:
        return unstructured

    # Fetch environment variables
    assert (
        unstructured_base_url := app.config.get("UNSTRUCTURED_BASE_URL")
    ), "SHAREPOINT_UNSTRUCTURED_BASE_URL must be set"
    assert (
        api_key := app.config.get("UNSTRUCTURED_API_KEY")
    ), "SHAREPOINT_UNSTRUCTURED_API_KEY must be set"

    unstructured = UnstructuredRequestSession(unstructured_base_url, api_key)

    return unstructured
