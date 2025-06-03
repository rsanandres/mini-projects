import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendScraper:
    def __init__(self):
        self.sources = {
            "arxiv": "https://arxiv.org/list/cs.AI/recent",
            "papers_with_code": "https://paperswithcode.com/latest",
            "huggingface": "https://huggingface.co/models"
        }
    
    def scrape_arxiv(self) -> List[Dict]:
        """Scrape latest AI papers from arXiv."""
        try:
            response = requests.get(self.sources["arxiv"])
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []
            
            # Extract paper titles and links
            for item in soup.find_all("div", class_="list-title"):
                title = item.text.strip()
                papers.append({
                    "title": title,
                    "source": "arxiv",
                    "type": "research_paper"
                })
            
            return papers
        except Exception as e:
            logger.error(f"Error scraping arXiv: {str(e)}")
            return []

    def scrape_papers_with_code(self) -> List[Dict]:
        """Scrape trending papers from Papers with Code."""
        try:
            response = requests.get(self.sources["papers_with_code"])
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []
            
            # Extract paper information
            for item in soup.find_all("div", class_="paper-card"):
                title = item.find("h1").text.strip()
                papers.append({
                    "title": title,
                    "source": "papers_with_code",
                    "type": "research_paper"
                })
            
            return papers
        except Exception as e:
            logger.error(f"Error scraping Papers with Code: {str(e)}")
            return []

    def get_all_trends(self) -> List[Dict]:
        """Get trends from all sources."""
        all_trends = []
        all_trends.extend(self.scrape_arxiv())
        all_trends.extend(self.scrape_papers_with_code())
        return all_trends

if __name__ == "__main__":
    scraper = TrendScraper()
    trends = scraper.get_all_trends()
    print(f"Found {len(trends)} trends") 