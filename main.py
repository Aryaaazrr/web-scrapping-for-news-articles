import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from typing import List, Dict, Optional
import json

class Scrapping:
    def __init__(self, delay: float = 1.0):
        self.base_url = "https://www.detik.com"
        self.search_url = "https://www.detik.com/search/searchall"
        self.delay = delay
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[requests.Response]:
        try:
            if params is None:
                params = {} 

            # choose your condition params for search query scrapping in url
            # params['result_type'] = 'relevansi' 
            params['result_type'] = 'latest'
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = ' '.join(text.split())
        return text.strip()

    def _extract_publication_time(self, article_elem) -> str:
        time_elem = article_elem.select_one('.media__date')
        if time_elem:
            return self._clean_text(time_elem.get_text())
        return ""

    def _extract_image_url(self, article_elem) -> str:
        img_selectors = article_elem.select_one('.media__image img')
        
        if img_selectors:
            for attr in ['src', 'data-src', 'data-lazy-src']:
                img_url = img_selectors.get(attr)
                if img_url:
                    return urljoin(self.base_url, img_url)
        return ""

    def _is_advertisement(self, article_elem) -> bool:
        ads_elem = article_elem.select_one('.ads-slot-mb-container')
        if ads_elem:
            return True
        return False

    def _extract_article_data(self, article_elem) -> Optional[Dict[str, str]]:
        try:
            if self._is_advertisement(article_elem):
                return None
            
            title_selectors = [
                '.media__title a',
                '.title a',
                'h2 a',
                'h3 a',
                'a[class*="title"]'
            ]
            
            title = ""
            body_text = ""
            
            for selector in title_selectors:
                title_elem = article_elem.select_one(selector)
                if title_elem:
                    title = self._clean_text(title_elem.get_text())
                    break
            
            if not title:
                return None
            
            body_elem = article_elem.select_one('.media__desc')
            
            if body_elem:
                body_text = self._clean_text(body_elem.get_text())
            else:
                body_text = "[No body text available]"

            image_url = self._extract_image_url(article_elem)
            pub_time = self._extract_publication_time(article_elem)
            
            return {
                'title': title,
                'image_link': image_url,
                'body_text': body_text,
                'publication_time': pub_time
            }
            
        except Exception as e:
            print(f"Error extracting article data: {e}")
            return None

    def search(self, query: str, max_pages: int = 3) -> List[Dict[str, str]]:
        results = []
        
        print(f"Starting search for: '{query}'")
        print(f"Will scrape up to {max_pages} pages")
        
        for page in range(1, max_pages + 1):
            print(f"\n--- Scraping page {page} ---")
            
            params = {
                'query': query,
                'page': page
            }
            
            response = self._make_request(self.search_url, params)
            if not response:
                print(f"Failed to fetch page {page}")
                continue
            
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                print(f"Error parsing HTML for page {page}: {e}")
                continue

            article_selectors = [
                'article',
                '.list-content__item',
                '.media',
                '[class*="article"]',
                '[class*="item"]'
            ]
            
            articles_found = []
            for selector in article_selectors:
                articles_found = soup.select(selector)
                if articles_found:
                    break
            
            if not articles_found:
                print(f"No articles found on page {page}")
                continue
            
            print(f"Found {len(articles_found)} potential articles on page {page}")
            
            page_results = []
            for i, article in enumerate(articles_found):
                article_data = self._extract_article_data(article)
                if article_data:
                    page_results.append(article_data)
                    print(f"  ✅ Extracted article {len(page_results)}: {article_data['title'][:50]}...")
                else:
                    print(f"  ❌ Skipped article {i+1} (ad or extraction failed)")
            
            results.extend(page_results)
            print(f"Page {page} completed. Found {len(page_results)} valid articles.")
            
            if page < max_pages:
                print(f"Waiting {self.delay} seconds before next page...")
                time.sleep(self.delay)
        
        print(f"\n=== Search completed ===")
        print(f"Total articles found: {len(results)}")
        return results

    def save_results(self, results: List[Dict[str, str]], filename: str = "detik_search_results.json"):

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

    def print_results(self, results: List[Dict[str, str]], limit: int = 5):

        print(f"\n=== Search Results (showing first {min(limit, len(results))} of {len(results)}) ===")
        
        for i, article in enumerate(results[:limit], 1):
            print(f"\n--- Article {i} ---") 
            print(f"Title: {article['title']}")
            print(f"Image URL: {article['image_link']}")
            print(f"Body Text: {article['body_text'][:200]}..." if len(article['body_text']) > 200 else f"Body Text: {article['body_text']}")
            print(f"Publication Time: {article['publication_time']}")
            print("-" * 80)


def main():

    scraper = Scrapping(delay=1.5)  
    
    query = input("Enter search query: ").strip()
    if not query:
        print("No query. Using default query: 'teknologi'")
        query = "teknologi"
    
    try:
        max_pages = int(input("Enter number of pages to scrape (1-3, default 3): ") or "3")
        max_pages = max(1, min(3, max_pages)) 
    except ValueError:
        max_pages = 3
        print("Invalid input. Using default: 3 pages")
    
    results = scraper.search(query, max_pages=max_pages)
    
    if results:
        scraper.print_results(results, limit=10)
        
        filename = f"detik_search_{query.replace(' ', '_')}.json"
        scraper.save_results(results, filename)
        
        print(f"\nScraping completed successfully!")
        print(f"Found {len(results)} articles across {max_pages} pages")
    else:
        print("No results found. Please try a different search query.")


main() 