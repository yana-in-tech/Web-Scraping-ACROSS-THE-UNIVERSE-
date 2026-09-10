import requests

params = {
    "action": "query",
    "list": "search",
    "srsearch": "machine learning",
    "format": "json",
    "srlimit": 5,
}

response = requests.get(
    "https://en.wikipedia.org/w/api.php",
    params=params,
    headers={
        "User-Agent": "WikipediaExample/1.0 (your-email@example.com)"
    },
    timeout=20,
)

response.raise_for_status()
data = response.json()

for result in data["query"]["search"]:
    print(result["title
    "])
