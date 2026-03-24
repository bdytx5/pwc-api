# Papers With Code - Star Tracker

Daily-updated dataset of ML/AI papers with GitHub repos and star growth stats.

## Data

Two datasets are available:

| File | What's in it |
|------|-------------|
| `papers_with_stats.json` | Arxiv papers that have a linked GitHub repo (paper required) |
| `ai_repos_with_stats.json` | All trending AI/ML repos — with or without a paper |

### `papers_with_stats.json`

```json
{
  "arxiv_url": "https://arxiv.org/abs/2412.19437",
  "title": "DeepSeek-V3 Technical Report",
  "github_url": "https://github.com/deepseek-ai/DeepSeek-V3",
  "stars": 102289,
  "date_published": "2024-12-27",
  "first_seen": "2025-08-13",
  "stars_3d_gain": 62,
  "stars_7d_gain": 144,
  "stars_14d_gain": 356,
  "stars_30d_gain": 660,
  "stars_60d_gain": 1065,
  "stars_90d_gain": 1486,
  "stars_180d_gain": null
}
```

### `ai_repos_with_stats.json`

```json
{
  "github_url": "https://github.com/owner/repo",
  "name": "repo-name",
  "description": "Repo description",
  "stars": 1234,
  "topics": ["machine-learning", "pytorch"],
  "language": "Python",
  "has_paper": true,
  "arxiv_url": "https://arxiv.org/abs/2501.12345",
  "date_created": "2026-03-20",
  "first_seen": "2026-03-25",
  "stars_3d_gain": 100,
  "stars_7d_gain": 250,
  "stars_14d_gain": null,
  "stars_30d_gain": null,
  "stars_60d_gain": null,
  "stars_90d_gain": null,
  "stars_180d_gain": null
}
```

## Install

```bash
pip install git+https://github.com/bdytx5/pwc-api.git
```

## Quick start

```python
from pwc_papers import search

# Most popular AI repos released this year
results = search(source="repos", top_n=25, sort_by="stars", date_from="2026-01-01")
for r in results:
    print(f"{r['stars']:>6}  {r['name']:30s}  {r['date_created']}  {r['description'][:50]}")
```

## API Reference

### `search(source, top_n, sort_by, date_from, date_to)`

Unified search across both datasets with filtering and sorting.

```python
from pwc_papers import search
```

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `source` | str | `"papers"` | `"papers"` for arxiv papers with repos, `"repos"` for all AI repos |
| `top_n` | int | `50` | Number of results to return |
| `sort_by` | str | `"stars"` | Sort field (see below) |
| `date_from` | str | `None` | Filter: publish/creation date >= this (`"YYYY-MM-DD"`) |
| `date_to` | str | `None` | Filter: publish/creation date <= this (`"YYYY-MM-DD"`) |

**Sort options:** `"stars"`, `"stars_3d_gain"`, `"stars_7d_gain"`, `"stars_14d_gain"`, `"stars_30d_gain"`, `"stars_60d_gain"`, `"stars_90d_gain"`, `"stars_180d_gain"`

### Examples

```python
from pwc_papers import search

# --- Choosing source: papers vs repos ---

# Papers only (must have arxiv link + github repo)
papers = search(source="papers", top_n=10, sort_by="stars")

# AI repos (any trending AI/ML repo, paper optional)
repos = search(source="repos", top_n=10, sort_by="stars")

# --- Sorting by different star gains ---

# Hottest papers this week
search(source="papers", top_n=10, sort_by="stars_7d_gain")

# Fastest growing repos this month
search(source="repos", top_n=10, sort_by="stars_30d_gain")

# Most stars gained in last 3 days
search(source="repos", top_n=10, sort_by="stars_3d_gain")

# --- Date filtering ---

# Most popular AI repos released this year
search(source="repos", top_n=25, sort_by="stars", date_from="2026-01-01")

# Papers published in Q1 2026
search(source="papers", top_n=20, sort_by="stars", date_from="2026-01-01", date_to="2026-03-31")

# Repos created in the last 30 days, sorted by star velocity
search(source="repos", top_n=15, sort_by="stars_7d_gain", date_from="2026-02-22")

# --- Combining filters ---

# Top repos from the past year with fastest weekly growth
search(
    source="repos",
    top_n=20,
    sort_by="stars_7d_gain",
    date_from="2025-03-24",
    date_to="2026-03-24",
)
```

### Convenience functions

```python
from pwc_papers import load_papers, trending, load_ai_repos, trending_repos

# Load raw data
all_papers = load_papers()       # list of dicts, sorted by stars
all_repos = load_ai_repos()      # list of dicts, sorted by stars

# Trending by star gain window
hot_papers = trending(days=7, top_n=20)       # papers by 7-day gain
hot_repos = trending_repos(days=30, top_n=20) # repos by 30-day gain
```

### curl

```bash
# Papers
curl -s https://raw.githubusercontent.com/bdytx5/pwc-api/main/papers_with_stats.json | python3 -m json.tool | head -30

# AI Repos
curl -s https://raw.githubusercontent.com/bdytx5/pwc-api/main/ai_repos_with_stats.json | python3 -m json.tool | head -30
```

## Update frequency

Data is rebuilt and pushed daily at ~2am UTC.
