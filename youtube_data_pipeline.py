import asyncio
import logging
from youtube_scraper import YouTubeScraper
from youtube_parser import YouTubeParser
from google_sheet_writer import GoogleSheetWriter

logging.basicConfig(level=logging.INFO)


class YouTubeDataPipeline:
    def __init__(self, video_urls=['url_1', 'url_2'], # Заменить на свои значения
                 spreadsheet_id='spreadsheet_id'): # Заменить на свое значение
        self.scraper = YouTubeScraper(video_urls)
        self.parser = YouTubeParser()
        self.writer = GoogleSheetWriter(spreadsheet_id)

    async def run(self):
        logging.info("Starting YouTube data pipeline...")
        html_data = await self.scraper.get_video_data()
        parsed_data = []
        for html in html_data:
            parsed_data.append(await self.parser.parse(html))
        await self.writer.write_to_sheet(parsed_data)
        logging.info("Pipeline completed!")


pipeline = YouTubeDataPipeline()
asyncio.run(pipeline.run())