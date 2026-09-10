import requests

title = "Python (programming language)"
url_title = title.replace(" ", "_")

url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{url_title}"

response = requests.get(
    url,
    headers={
        "User-Agent": "WikipediaExample/1.0 (your-email@example.com)"
    },
    timeout=20,
)

response.raise_for_status()
data = response.json()

print("Title:", data["title"])
print("Description:", data.get("description"))
print("Summary:", data["extract"])
print("Article URL:", data["content_urls"]["desktop"]["pag
e"])
