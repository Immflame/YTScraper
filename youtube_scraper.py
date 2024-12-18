import asyncio
import logging
import aiohttp

logging.basicConfig(level=logging.INFO)


class YouTubeScraper:
    def __init__(self, video_urls):
        self.video_urls = video_urls

    async def fetch_html(self, url, session):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()
                logging.info(f"Successfully fetched HTML for {url}")
                return html_content
        except aiohttp.ClientError as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    async def get_video_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_html(url, session) for url in self.video_urls]
            return await asyncio.gather(*tasks)
