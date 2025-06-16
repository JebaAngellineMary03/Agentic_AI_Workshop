import requests

def get_citation_count(title):
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"title.search:{title}",
        "per-page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("meta", {}).get("count", "Citation info not found")
    return "Citation info not found"
