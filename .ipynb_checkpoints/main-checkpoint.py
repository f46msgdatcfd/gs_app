from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import os
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

app = FastAPI(title="Google Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def google_search_all_results(
    search_terms: str,
    mustinclude_terms: str = None,
    ui_language: str = None,
    content_language: str = None,
    exclude_terms: str = None,
    or_terms: str = None,
    start_date: str = None,
    end_date: str = None,
    server_country: str = None,
    user_location: str = None,
    max_results: int = 100
):
    all_results = []
    results_per_page = 10
    start_index = 1
    filter_dup = "1"
    max_results = min(max_results, 100)

    if not API_KEY or not SEARCH_ENGINE_ID:
        raise RuntimeError("Missing GOOGLE_API_KEY or SEARCH_ENGINE_ID in environment.")

    while len(all_results) < max_results:
        url = (
            f"https://www.googleapis.com/customsearch/v1?q={quote(search_terms)}"
            f"&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
            f"&filter={filter_dup}"
            f"{f'&gl={quote(user_location)}' if user_location and user_location != 'null' else ''}"
            f"{f'&cr={quote(server_country)}' if server_country and server_country != 'null' else ''}"
            f"{f'&exactTerms={quote(mustinclude_terms)}' if mustinclude_terms and mustinclude_terms != 'null' else ''}"
            f"{f'&excludeTerms={quote(exclude_terms)}' if exclude_terms and exclude_terms != 'null' else ''}"
            f"{f'&orTerms={quote(or_terms)}' if or_terms and or_terms != 'null' else ''}"
            f"{f'&sort=date:r:{start_date}:{end_date}' if start_date and end_date and start_date != 'null' and end_date != 'null' else ''}"
            f"{f'&hl={quote(ui_language)}' if ui_language and ui_language != 'null' else ''}"
            f"{f'&lr={quote(content_language)}' if content_language and content_language != 'null' else ''}"
            f"&start={start_index}&num={results_per_page}"
        )

        print(f"[DEBUG] Requesting: {url}")

        try:
            response = requests.get(url)
            print(f"[DEBUG] Status: {response.status_code}")
            response.raise_for_status()
            data = response.json()

            if "items" not in data:
                print("[INFO] No items in response.")
                break

            for item in data["items"]:
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                snippet = item.get("snippet", "No snippet")
                all_results.append({"title": title, "link": link, "snippet": snippet})
                if len(all_results) >= max_results:
                    break

            start_index += results_per_page
            if start_index > 91:
                break

            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            break

    return all_results[:max_results]

@app.get("/search")
async def search(
    search_terms: str = None,
    mustinclude_terms: str = None,
    ui_language: str = None,
    content_language: str = None,
    exclude_terms: str = None,
    or_terms: str = None,
    start_date: str = None,
    end_date: str = None,
    server_country: str = None,
    user_location: str = None,
    max_results: int = 100
):
    results = google_search_all_results(
        search_terms=search_terms,
        mustinclude_terms=mustinclude_terms,
        ui_language=ui_language,
        content_language=content_language,
        exclude_terms=exclude_terms,
        or_terms=or_terms,
        start_date=start_date,
        end_date=end_date,
        server_country=server_country,
        user_location=user_location,
        max_results=max_results
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
