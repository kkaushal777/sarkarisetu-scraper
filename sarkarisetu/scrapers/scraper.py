"""Main scraper for SarkariResult.com.cm"""
import httpx
import re
import json
from datetime import datetime
from selectolax.parser import HTMLParser
from typing import List, Dict, Optional


class SarkariScraper:
    """Unified scraper for all SarkariResult pages"""
    
    def __init__(self, url: str):
        self.url = url
        self.base_url = "https://sarkariresult.com.cm"
        self.timeout = 30
        self.headers = {
            "User-Agent": "SarkariSetuBot/1.0 (+contact: dev@sarkarisetu.com)"
        }
    
    def fetch(self) -> str:
        """Fetch page HTML"""
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(self.url, headers=self.headers)
                resp.raise_for_status()
                print(f"[+] Fetched {self.url}")
                return resp.text
        except Exception as e:
            print(f"[!] Error fetching {self.url}: {e}")
            raise
    
    def scrape_aggregator_list(self) -> Dict:
        """Scrape aggregator list pages (jobs, results, admit cards, answer keys)"""
        html = self.fetch()
        tree = HTMLParser(html)
        
        # Extract title and description
        title = tree.css_first("h1")
        title_text = title.text().strip() if title else None
        
        # Extract items from list
        items = []
        rank = 1
        
        for li in tree.css("li"):
            link = li.css_first("a[href]")
            if not link:
                continue
            
            link_text = link.text().strip()
            link_url = link.attributes.get("href", "").strip()
            full_text = li.text().strip()
            
            if not link_text or not link_url:
                continue
            
            # Parse metadata
            metadata_type = None
            metadata_value = None
            status_text = None
            
            if "Last Date:" in full_text:
                metadata_type = "last_date"
                match = re.search(r'Last Date:\s*(\d+\s+\w+\s+\d{4})', full_text)
                if match:
                    metadata_value = match.group(1)
                    status_text = "Active"
            elif "– Out" in link_text:
                metadata_type = "status"
                metadata_value = "out"
                status_text = "Out"
            elif "– Pending" in link_text:
                metadata_type = "status"
                metadata_value = "pending"
                status_text = "Pending"
            
            items.append({
                "rank": rank,
                "title": link_text,
                "link": link_url,
                "metadata_type": metadata_type,
                "metadata_value": metadata_value,
                "status_text": status_text
            })
            rank += 1
        
        return {
            "url": self.url,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "title": title_text,
            "items_count": len(items),
            "items": items
        }
    
    def scrape_recruitment_detail(self) -> Dict:
        """Scrape detailed recruitment pages"""
        html = self.fetch()
        tree = HTMLParser(html)
        
        # Extract title
        title = tree.css_first("h1")
        title_text = title.text().strip() if title else None
        
        # Extract tables
        tables = {}
        for table in tree.css("table"):
            # Find preceding heading
            heading = None
            prev = table.parent
            while prev:
                h = prev.css_first("h2, h3, h4")
                if h:
                    heading = h.text().strip()
                    break
                prev = prev.parent
            
            # Extract table rows
            rows = []
            for tr in table.css("tr"):
                cells = []
                for td in tr.css("td, th"):
                    cells.append(td.text().strip())
                if cells:
                    rows.append(cells)
            
            if rows and heading:
                tables[heading] = rows
        
        # Extract all links
        links = []
        for a in tree.css("a[href]"):
            text = a.text().strip()
            url = a.attributes.get("href", "").strip()
            if text and url and len(text) > 3:
                links.append({"text": text, "url": url})
        
        return {
            "url": self.url,
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "title": title_text,
            "tables": tables,
            "links_count": len(links),
            "important_links": [l for l in links if any(k in l["text"].lower() for k in ["apply", "official", "notification", "admit", "result"])]
        }


# Quick usage examples
if __name__ == "__main__":
    # Test aggregator scraping
    print("Testing Aggregator Scraper...\n")
    
    scraper = SarkariScraper("https://sarkariresult.com.cm/latest-jobs/")
    result = scraper.scrape_aggregator_list()
    print(f"Title: {result['title']}")
    print(f"Total items: {result['items_count']}")
    print(f"First 3 items:")
    for item in result['items'][:3]:
        print(f"  - {item['title']} ({item['status_text']})")
    
    print("\n" + "="*80 + "\n")
    
    # Test detail scraping
    print("Testing Detail Page Scraper...\n")
    scraper2 = SarkariScraper("https://sarkariresult.com.cm/up-police-constable-recruitment-2026/")
    result2 = scraper2.scrape_recruitment_detail()
    print(f"Title: {result2['title']}")
    print(f"Tables found: {len(result2['tables'])}")
    print(f"Important links: {len(result2['important_links'])}")
    if result2['important_links']:
        print(f"First link: {result2['important_links'][0]}")
