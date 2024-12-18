import asyncio
import logging
from youtube_scraper import YouTubeScraper
from youtube_parser import YouTubeParser
from google_sheet_writer import GoogleSheetWriter

logging.basicConfig(level=logging.INFO)


class YouTubeDataPipeline:
    def __init__(self, video_urls=['https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'https://www.youtube.com/watch?v=9bZkp7q19f0'],
                 spreadsheet_id='1hhKl_UliaVWZiSOx599rmdm-_Z_fKPEiV4-tfN7VWek'):
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