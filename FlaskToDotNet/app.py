# app.py (Flask Microservice)
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import httpx

app = Flask(__name__)

# The internal URL of our high-performance .NET API Gateway
DOTNET_GATEWAY_URL = "http://localhost:5123/api/data-ingestion"

@app.route('/scrape', methods=['POST'])
async def handle_scrape_request():
    # Receive target URL from ASP.NET Core scheduler
    request_data = request.get_json() or {}
    target_url = request_data.get("url", "https://ycombinator.com")

    try:
        # 1. Fetch the remote website asynchronously
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()

        # 2. Parse and structure the data (Example: Scraping Hacker News links)
        soup = BeautifulSoup(response.text, 'html.parser')
        scraped_items = []

        for row in soup.find_all('tr', class_='athing'):
            title_line = row.find('span', class_='titleline')
            if title_line and title_line.find('a'):
                link_element = title_line.find('a')
                scraped_items.append({
                    "id": row.get('id'),
                    "title": link_element.text,
                    "url": link_element.get('href')
                })

        # 3. Securely forward the clean, structured data directly to ASP.NET Core
        async with httpx.AsyncClient() as client:
            dotnet_response = await client.post(
                DOTNET_GATEWAY_URL, 
                json={"sourceUrl": target_url, "items": scraped_items},
                headers={"X-Internal-Secret": "SuperSecureToken123"} # Basic internal auth
            )
            dotnet_response.raise_for_status()

        return jsonify({
            "status": "success", 
            "itemsProcessed": len(scraped_items),
            "gatewayResponse": "Data delivered to .NET successfully."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(p
            ort=5001)
