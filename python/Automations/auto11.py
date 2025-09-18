# Simple web scraping example: fetch headlines from a news site
import requests
from bs4 import BeautifulSoup



def scrape_headlines(url, tags=['h2']):
	try:
		response = requests.get(url, timeout=10)
		response.raise_for_status()
	except requests.RequestException as e:
		print(f"Error fetching {url}: {e}")
		return []
	soup = BeautifulSoup(response.text, 'html.parser')
	headlines = []
	for tag in tags:
		for elem in soup.find_all(tag):
			text = elem.get_text(strip=True)
			link = elem.find('a')
			url_ref = link['href'] if link and link.has_attr('href') else None
			if text:
				headlines.append({'text': text, 'url': url_ref})
	return headlines

import re

def is_valid_url(url):
	return re.match(r"^https?://", url)

if __name__ == "__main__":
	default_url = "https://news.ycombinator.com/"
	while True:
		url = input(f"Enter the URL to scrape (default: {default_url}): ").strip()
		if not url:
			url = default_url
		if is_valid_url(url):
			break
		else:
			print("Please enter a valid URL starting with http:// or https://")

	tags_input = input("Enter tags to scrape (comma separated, default: h2): ").strip()
	tags = [t.strip() for t in tags_input.split(',') if t.strip()] if tags_input else ['h2']
	headlines = scrape_headlines(url, tags)
	print(f"\nFound {len(headlines)} headlines/snippets:")
	for h in headlines:
		if h['url']:
			print(f"- {h['text']} (URL: {h['url']})")
		else:
			print(f"- {h['text']}")

	save = input("Save results to file? (y/n): ").strip().lower()
	if save == 'y':
		filename = input("Enter filename (default: headlines.txt): ").strip() or "headlines.txt"
		try:
			with open(filename, 'w', encoding='utf-8') as f:
				for h in headlines:
					if h['url']:
						f.write(f"{h['text']} (URL: {h['url']})\n")
					else:
						f.write(f"{h['text']}\n")
			print(f"Results saved to {filename}")
		except Exception as e:
			print(f"Error saving file: {e}")
