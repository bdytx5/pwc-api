"""Client to fetch ML/AI papers and repos with star stats from the pwc-api repo."""

import json
import urllib.request
from datetime import datetime

_PAPERS_URL = "https://raw.githubusercontent.com/bdytx5/pwc-api/main/papers_with_stats.json"
_AI_REPOS_URL = "https://raw.githubusercontent.com/bdytx5/pwc-api/main/ai_repos_with_stats.json"


def _fetch(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())


# --- Papers (arxiv + github) ---

def load_papers(url=None):
    """Fetch and return the full list of papers with stats.

    Returns a list of dicts, sorted by stars descending.
    """
    return _fetch(url or _PAPERS_URL)


def trending(days=7, top_n=20, url=None):
    """Return top papers by star gain over the given window.

    Args:
        days: One of 3, 7, 14, 30, 60, 90, 180
        top_n: How many to return
    """
    key = f"stars_{days}d_gain"
    papers = load_papers(url)
    return sorted(papers, key=lambda p: p.get(key) or 0, reverse=True)[:top_n]


# --- AI Repos (with or without papers) ---

def load_ai_repos(url=None):
    """Fetch and return the full list of AI repos with stats.

    Returns a list of dicts, sorted by stars descending.
    """
    return _fetch(url or _AI_REPOS_URL)


def trending_repos(days=7, top_n=20, url=None):
    """Return top AI repos by star gain over the given window.

    Args:
        days: One of 3, 7, 14, 30, 60, 90, 180
        top_n: How many to return
    """
    key = f"stars_{days}d_gain"
    repos = load_ai_repos(url)
    return sorted(repos, key=lambda r: r.get(key) or 0, reverse=True)[:top_n]


# --- Unified search ---

def search(source="papers", top_n=50, sort_by="stars",
           date_from=None, date_to=None, url=None):
    """Search papers or AI repos with filtering and sorting.

    Args:
        source: "papers" for arxiv papers with repos, "repos" for all AI repos
        top_n: Number of results to return
        sort_by: "stars", "stars_3d_gain", "stars_7d_gain", "stars_14d_gain",
                 "stars_30d_gain", "stars_60d_gain", "stars_90d_gain", "stars_180d_gain"
        date_from: Filter by publish/creation date >= this (str "YYYY-MM-DD")
        date_to: Filter by publish/creation date <= this (str "YYYY-MM-DD")

    Returns:
        List of dicts sorted by sort_by descending.
    """
    if source == "papers":
        data = load_papers(url)
        date_field = "date_published"
    elif source == "repos":
        data = load_ai_repos(url)
        date_field = "date_created"
    else:
        raise ValueError(f"source must be 'papers' or 'repos', got '{source}'")

    # Date filtering
    if date_from or date_to:
        filtered = []
        for item in data:
            d = item.get(date_field)
            if not d or d == "Unknown":
                continue
            if date_from and d < date_from:
                continue
            if date_to and d > date_to:
                continue
            filtered.append(item)
        data = filtered

    # Sort
    data.sort(key=lambda x: x.get(sort_by) or 0, reverse=True)

    return data[:top_n]
