import os
import re
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class YCCompanyScraper:
    def __init__(self):
        self.base_url = "https://www.ycombinator.com/companies"
        self.companies: List[Dict] = []
        self.session: Optional[aiohttp.ClientSession] = None

    async def init_session(self):
        """Initialize aiohttp session with headers"""
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()

    def sanitize_filename(self, name: str) -> str:
        """Convert company name to valid directory name"""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.strip('_')

    async def fetch_companies(self) -> List[Dict]:
        """Fetch companies from YCombinator website"""
        try:
            async with self.session.get(f"{self.base_url}?isHiring=true") as response:
                if response.status == 200:
                    html = await response.text()
                    print("HTML Content:", html[:1000])  # Print first 1000 characters for debugging
                    
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Try different selectors
                    company_cards = soup.find_all('div', class_='company-card')
                    if not company_cards:
                        company_cards = soup.find_all('div', class_='company')
                    if not company_cards:
                        company_cards = soup.find_all('div', {'data-test': 'company-card'})
                    
                    print(f"Found {len(company_cards)} company cards")
                    
                    for card in company_cards:
                        print("Card HTML:", card.prettify()[:200])  # Print first 200 characters of each card
                        
                        company = {
                            'name': card.find('h3').text.strip() if card.find('h3') else 'Unknown',
                            'description': card.find('p').text.strip() if card.find('p') else '',
                            'url': card.find('a')['href'] if card.find('a') else '',
                            'batch': card.find('div', class_='batch').text.strip() if card.find('div', class_='batch') else 'Unknown'
                        }
                        self.companies.append(company)
                    
                    return self.companies
                else:
                    logging.error(f"Failed to fetch companies. Status code: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Error fetching companies: {str(e)}")
            return []

    async def process_company(self, company: Dict):
        """Process individual company data and create necessary files"""
        company_dir = self.sanitize_filename(company['name'])
        os.makedirs(company_dir, exist_ok=True)

        # Create summary.txt
        with open(os.path.join(company_dir, 'summary.txt'), 'w') as f:
            f.write(f"{company['name']} is a YCombinator company from the {company['batch']} batch. ")
            f.write(f"{company['description']}")

        # Determine if we should create market research or AI model
        # For now, we'll create market research for all companies
        # This can be enhanced later with AI detection
        self.create_market_research(company_dir, company)

    def create_market_research(self, company_dir: str, company: Dict):
        """Create market research markdown file"""
        with open(os.path.join(company_dir, 'market_research.md'), 'w') as f:
            f.write(f"# {company['name']} Market Research\n\n")
            f.write("## Company Overview\n")
            f.write(f"{company['description']}\n\n")
            f.write("## Target Market\n")
            f.write("To be researched and filled in.\n\n")
            f.write("## Key Competitors\n")
            f.write("To be researched and filled in.\n\n")
            f.write("## Recent Developments\n")
            f.write("To be researched and filled in.\n\n")
            f.write("## Potential AI Use Cases\n")
            f.write("To be researched and filled in.\n\n")

    async def create_test_companies(self):
        """Create test company folders for development"""
        test_companies = [
            {
                'name': 'Test Company 1',
                'description': 'A test company focused on AI research',
                'batch': 'W24',
                'url': 'https://example.com/company1'
            },
            {
                'name': 'Test Company 2',
                'description': 'A test company focused on blockchain technology',
                'batch': 'S24',
                'url': 'https://example.com/company2'
            }
        ]
        
        for company in test_companies:
            await self.process_company(company)

async def main():
    scraper = YCCompanyScraper()
    await scraper.init_session()
    
    try:
        # Create test companies for development
        await scraper.create_test_companies()
        
        # Uncomment the following lines when ready to scrape real data
        # companies = await scraper.fetch_companies()
        # logging.info(f"Found {len(companies)} companies")
        # for company in tqdm(companies, desc="Processing companies"):
        #     await scraper.process_company(company)
            
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
    finally:
        await scraper.close_session()

if __name__ == "__main__":
    asyncio.run(main()) 