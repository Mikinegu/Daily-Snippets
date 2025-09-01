# Simple web scraping example: fetch headlines from a news site
import requests
from bs4 import BeautifulSoup

def scrape_headlines(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	# Example: find all <h2> tags (common for headlines)
	headlines = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
	return headlines

if __name__ == "__main__":
	url = "https://news.ycombinator.com/"  
	headlines = scrape_headlines(url)
	print("Headlines:")
	for headline in headlines:
		print("-", headline)
