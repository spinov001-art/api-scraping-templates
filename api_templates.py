#!/usr/bin/env python3
"""
API Scraping Templates — Copy-paste templates for common API patterns.
REST, GraphQL, paginated, authenticated, rate-limited — all covered.
"""

import json
import time
import urllib.request
import urllib.parse
from typing import Generator


# ============================================================
# Template 1: Simple REST API (no auth)
# ============================================================
def scrape_rest_api(base_url: str, endpoint: str, params: dict = None) -> dict:
    """Basic REST GET request."""
    url = base_url + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "API-Scraper/1.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())


# ============================================================
# Template 2: Paginated API (offset-based)
# ============================================================
def scrape_paginated(base_url: str, per_page: int = 100, max_pages: int = 10) -> Generator:
    """Paginate through offset-based API results."""
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}&per_page={per_page}"
        req = urllib.request.Request(url, headers={"User-Agent": "API-Scraper/1.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        if not data:
            break
        yield from data
        time.sleep(0.5)  # Be respectful


# ============================================================
# Template 3: Cursor-based pagination
# ============================================================
def scrape_cursor_paginated(base_url: str, cursor_field: str = "cursor", max_items: int = 1000) -> list:
    """Paginate through cursor-based API results."""
    results = []
    cursor = None
    while len(results) < max_items:
        url = base_url
        if cursor:
            sep = "&" if "?" in url else "?"
            url += f"{sep}{cursor_field}={cursor}"
        req = urllib.request.Request(url, headers={"User-Agent": "API-Scraper/1.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        items = data.get("data", data.get("results", data.get("items", [])))
        if not items:
            break
        results.extend(items)
        cursor = data.get("next_cursor", data.get("cursor", data.get("next")))
        if not cursor:
            break
        time.sleep(0.5)
    return results[:max_items]


# ============================================================
# Template 4: Rate-limited API with retry
# ============================================================
def scrape_with_retry(url: str, max_retries: int = 3, headers: dict = None) -> dict:
    """Request with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers or {"User-Agent": "API-Scraper/1.0"})
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                wait = (2 ** attempt) + 1
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif e.code >= 500:  # Server error
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries: {url}")


# ============================================================
# Template 5: GraphQL API
# ============================================================
def scrape_graphql(endpoint: str, query: str, variables: dict = None, headers: dict = None) -> dict:
    """Send GraphQL query and return data."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={**(headers or {}), "Content-Type": "application/json", "User-Agent": "API-Scraper/1.0"}
    )
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())


# ============================================================
# Example usage
# ============================================================
if __name__ == "__main__":
    # Example: GitHub public API (no auth needed)
    print("=== REST API: GitHub user info ===")
    data = scrape_rest_api("https://api.github.com", "/users/torvalds")
    print(f"Name: {data['name']}, Repos: {data['public_repos']}, Followers: {data['followers']}")

    # Example: Paginated — Dev.to articles
    print("\n=== Paginated: Dev.to top articles ===")
    articles = list(scrape_paginated("https://dev.to/api/articles", per_page=5, max_pages=1))
    for a in articles[:3]:
        print(f"  {a['title'][:50]}... ({a['positive_reactions_count']} reactions)")

    print("\n=== GraphQL: GitHub API ===")
    result = scrape_graphql(
        "https://api.github.com/graphql",
        '{ viewer { login } }',
        headers={"Authorization": "bearer YOUR_TOKEN"}  # Replace with real token
    )
    print(f"  Result: {result}")
