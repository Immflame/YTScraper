import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class YouTubeParser:
    async def parse(self, html_content):
        try:
            if html_content is None:
                logging.warning("No HTML content to parse")
                return {}
            soup = BeautifulSoup(html_content, 'html.parser')
            video_data = {
                'title': self._get_meta_content(soup, 'name', 'title'),
                'description': self._get_meta_content(soup, 'name', 'description'),
                'tags': [tag['content'] for tag in soup.find_all('meta', property='og:video:tag')],
                'channel_name': self._get_meta_content(soup, 'itemprop', 'name', tag='link'),
                'views_number': self._get_meta_content(soup, 'itemprop', 'interactionCount'),
                'upload_date': self._get_meta_content(soup, 'itemprop', 'uploadDate'),
                'genre': self._get_meta_content(soup, 'itemprop', 'genre'),
            }
            logging.info("Successfully parsed video data")
            return video_data
        except (AttributeError, KeyError, TypeError) as e:
            logging.error(f"Error parsing HTML content: {e}")
            return {}

    def _get_meta_content(self, soup, attr1, attr2, tag='meta'):
        try:

            element = soup.find(tag, attrs={attr1: attr2})
            return element['content']

        except (AttributeError, TypeError):

            return None
