# API Scraping Templates — 20+ Ready-to-Use Python Scripts

> Copy-paste Python scripts for extracting data from popular APIs. No API keys needed for most.

Each template is a standalone script — just `pip install requests` and run.

> **Need custom data extraction?** I build production scrapers and data pipelines.
> [See my tools](https://github.com/spinov001-art/awesome-web-scraping-2026) | [Hire me](https://spinov001-art.github.io) | [Email](mailto:Spinov001@gmail.com)

## Templates

### YouTube (Innertube API — No Key)

```python
"""Extract YouTube comments without API key or quotas."""
import requests, json, re

def get_comments(video_id, max_comments=100):
    url = f"https://www.youtube.com/watch?v={video_id}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Extract continuation token from initial page
    match = re.search(r\'"continuation":"([^"]+)"\', resp.text)
    if not match:
        return []
    
    token = match.group(1)
    comments = []
    
    while token and len(comments) < max_comments:
        api_url = "https://www.youtube.com/youtubei/v1/next"
        payload = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240101"}},
            "continuation": token
        }
        r = requests.post(api_url, json=payload)
        data = r.json()
        # Parse comments from response...
        # (See full implementation in youtube-rag-knowledge-base repo)
        break
    
    return comments

# Usage
comments = get_comments("dQw4w9WgXcQ")
```

**Full RAG pipeline:** [youtube-rag-knowledge-base](https://github.com/spinov001-art/youtube-rag-knowledge-base)
**Tutorial:** [YouTube Innertube API Guide](https://github.com/spinov001-art/youtube-rag-knowledge-base)

---

### npm Registry (No Key)

```python
"""Search npm packages and get download stats."""
import requests

def search_npm(query, size=10):
    url = f"https://registry.npmjs.org/-/v1/search?text={query}&size={size}"
    return requests.get(url).json()["objects"]

def get_downloads(package, period="last-week"):
    url = f"https://api.npmjs.org/downloads/point/{period}/{package}"
    return requests.get(url).json()

# Find web scraping packages
results = search_npm("web scraping", size=5)
for pkg in results:
    name = pkg["package"]["name"]
    downloads = get_downloads(name)
    print(f"{name}: {downloads.get('downloads', 0):,} downloads/week")
```

**Tutorial:** [npm Registry API Guide](https://docs.npmjs.com/)

---

### arXiv (No Key)

```python
"""Search academic papers on arXiv."""
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    resp = requests.get(url)
    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    papers = []
    for entry in root.findall("atom:entry", ns):
        papers.append({
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip()[:200],
            "published": entry.find("atom:published", ns).text[:10],
        })
    return papers

papers = search_arxiv("large language models", max_results=3)
for p in papers:
    print(f"{p['published']} | {p['title']}")
```

**Tutorial:** [arXiv API Guide](https://arxiv.org/help/api)

---

### Crossref (130M+ Papers, No Key)

```python
"""Search academic papers with citation data."""
import requests

def search_crossref(query, rows=5):
    url = f"https://api.crossref.org/works?query={query}&rows={rows}"
    resp = requests.get(url, headers={"User-Agent": "ScrapingTemplates/1.0 (mailto:Spinov001@gmail.com)"})
    return resp.json()["message"]["items"]

papers = search_crossref("machine learning healthcare")
for p in papers:
    print(f"{p.get('title', ['?'])[0][:80]} | cited: {p.get('is-referenced-by-count', 0)}")
```

**Tutorial:** [Crossref API Guide](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

---

### Shodan InternetDB (No Key)

```python
"""Scan any IP for open ports and vulnerabilities."""
import requests

def scan_ip(ip):
    return requests.get(f"https://internetdb.shodan.io/{ip}").json()

result = scan_ip("8.8.8.8")
print(f"Ports: {result.get('ports', [])}")
print(f"Vulns: {result.get('vulns', [])}")
print(f"Hostnames: {result.get('hostnames', [])}")
```

---

### Have I Been Pwned (Password Check, No Key)

```python
"""Check if a password has been breached (k-anonymity — password never sent)."""
import requests, hashlib

def check_password(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    for line in resp.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0

count = check_password("password123")
print(f"Found in {count:,} breaches" if count else "Not found in any breach")
```

---

### Reddit JSON API (No Key)

```python
"""Extract Reddit data by adding .json to any URL."""
import requests

def get_subreddit(name, sort="hot", limit=10):
    url = f"https://www.reddit.com/r/{name}/{sort}.json?limit={limit}"
    resp = requests.get(url, headers={"User-Agent": "ScrapingBot/1.0"})
    posts = resp.json()["data"]["children"]
    return [{"title": p["data"]["title"], "score": p["data"]["score"]} for p in posts]

posts = get_subreddit("programming", limit=5)
for p in posts:
    print(f"{p['score']:>5} | {p['title'][:70]}")
```

---

### IP Geolocation (No Key)

```python
"""Get location data for any IP address."""
import requests

def geolocate(ip=""):
    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"
    return requests.get(url).json()

loc = geolocate("8.8.8.8")
print(f"{loc['country']}, {loc['city']} | ISP: {loc['isp']}")
```

---

## More APIs (No Key Required)

| API | Endpoint | What You Get |
|-----|----------|-------------|
| CoinGecko | `api.coingecko.com/api/v3/` | Crypto prices, 10K+ coins |
| Open-Meteo | `api.open-meteo.com/v1/forecast` | Weather, 16-day forecast |
| Open Library | `openlibrary.org/search.json` | 20M+ books |
| PyPI | `pypi.org/pypi/{pkg}/json` | Python packages |
| HTTPBin | `httpbin.org/` | HTTP testing |
| JSONPlaceholder | `jsonplaceholder.typicode.com/` | Fake REST API |
| Dog CEO | `dog.ceo/api/` | Random dog images |
| Countries REST | `restcountries.com/v3.1/` | Country data |

## Tutorials

- [Price Monitoring System with Free APIs](https://github.com/spinov001-art/api-scraping-templates) — Sitemaps + JSON-LD + GitHub as database = $0/month price tracker

## All My Projects

- [77 Web Scraping Tools](https://github.com/spinov001-art/awesome-web-scraping-2026) — Awesome list, 9 stars
- [YouTube RAG Pipeline](https://github.com/spinov001-art/youtube-rag-knowledge-base) — Build AI knowledge base from YouTube
- [Free API Collection](https://github.com/spinov001-art/free-api-collection) — 30+ APIs, no key
- [250+ Projects on GitHub](https://github.com/spinov001-art) — Web scraping, APIs, data extraction



---

## Author

Built by Alex Spinov — production-grade web scrapers and data tools.

- [88+ scrapers on Apify](https://apify.com/knotless_cadence) | Email: **spinov001@gmail.com**

## License

MIT — use these templates freely in your projects.
