# Papers With Code - Star Tracker

Daily-updated dataset of ML/AI papers with GitHub repos and star growth stats.

## Data

**`papers_with_stats.json`** — array of papers sorted by stars (descending).

Each entry:

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

| Field | Description |
|-------|-------------|
| `arxiv_url` | Link to the paper on arXiv |
| `title` | Paper title |
| `github_url` | Associated GitHub repo |
| `stars` | Current GitHub star count |
| `date_published` | Paper publication date |
| `first_seen` | When we first started tracking |
| `stars_Nd_gain` | Star count change over the last N days (null if insufficient history) |

## Usage

### curl

```bash
curl -s https://raw.githubusercontent.com/bdytx5/pwc-api/main/papers_with_stats.json | python3 -m json.tool | head -20
```

### Python

```python
import requests

papers = requests.get(
    "https://raw.githubusercontent.com/bdytx5/pwc-api/main/papers_with_stats.json"
).json()

# Top 10 by 7-day star gain
trending = sorted(papers, key=lambda p: p.get("stars_7d_gain") or 0, reverse=True)[:10]
for p in trending:
    print(f"{p['stars_7d_gain']:+5d}  {p['title'][:60]}")
```

### Install as a Python package

```bash
pip install git+https://github.com/bdytx5/pwc-api.git
```

Then:

```python
from pwc_papers import load_papers, trending

# All papers (sorted by stars desc)
papers = load_papers()

# Top 20 by 7-day star gain
hot = trending(days=7, top_n=20)
for p in hot:
    print(f"{p['stars_7d_gain']:+5d}  {p['title'][:60]}")
```

To upgrade to the latest data schema:

```bash
pip install --upgrade git+https://github.com/bdytx5/pwc-api.git
```

## Update frequency

Data is rebuilt and pushed daily.
