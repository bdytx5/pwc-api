"""Simple client to fetch papers with star stats from the pwc-api repo."""

import json
import urllib.request

_DEFAULT_URL = "https://raw.githubusercontent.com/bdytx5/pwc-api/main/papers_with_stats.json"


def load_papers(url=None):
    """Fetch and return the full list of papers with stats.

    Returns a list of dicts, sorted by stars descending.
    """
    url = url or _DEFAULT_URL
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())


def trending(days=7, top_n=20, url=None):
    """Return top papers by star gain over the given window.

    Args:
        days: One of 3, 7, 14, 30, 60, 90, 180
        top_n: How many to return
    """
    key = f"stars_{days}d_gain"
    papers = load_papers(url)
    return sorted(papers, key=lambda p: p.get(key) or 0, reverse=True)[:top_n]
