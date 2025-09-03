# Simple web scraping example: fetch headlines from a news site
import requests
from bs4 import BeautifulSoup


def scrape_headlines(url):
	try:
		response = requests.get(url, timeout=10)
		response.raise_for_status()
	except requests.RequestException as e:
		print(f"Error fetching {url}: {e}")
		return []
	soup = BeautifulSoup(response.text, 'html.parser')
	headlines = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
	return headlines

if __name__ == "__main__":
	url = input("Enter the URL to scrape headlines from (default: https://news.ycombinator.com/): ").strip()
	if not url:
		url = "https://news.ycombinator.com/"
	headlines = scrape_headlines(url)
	print(f"\nFound {len(headlines)} headlines:")
	for headline in headlines:
		print("-", headline)
