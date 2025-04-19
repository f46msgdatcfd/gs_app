from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import time
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Initialize FastAPI app
app = FastAPI(title="Google Search API")

# Mount static directory to serve HTML frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Enable CORS for frontend JS calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_google_search_url(
    search_terms: str,
    mustinclude_terms: str,
    ui_language: str,
    content_language: str,
    exclude_terms: str,
    or_terms: str,
    start_date: str,
    end_date: str,
    server_country: str,
    user_location: str,
    start_index: int,
    results_per_page: int = 10
) -> str:
    if not search_terms or search_terms.strip().lower() == "null":
        search_terms = ""
    url = (
        f"https://www.googleapis.com/customsearch/v1?q={quote(search_terms)}"
        f"&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        f"&filter=1"
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
    return url

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
    if not API_KEY or not SEARCH_ENGINE_ID:
        raise RuntimeError("Missing GOOGLE_API_KEY or SEARCH_ENGINE_ID in environment.")

    all_results = []
    results_per_page = 10
    start_index = 1
    max_results = min(max_results, 100)

    while len(all_results) < max_results:
        url = build_google_search_url(
            search_terms,
            mustinclude_terms,
            ui_language,
            content_language,
            exclude_terms,
            or_terms,
            start_date,
            end_date,
            server_country,
            user_location,
            start_index,
            results_per_page,
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
                all_results.append({
                    "title": item.get("title", "No title"),
                    "link": item.get("link", "No link"),
                    "snippet": item.get("snippet", "No snippet")
                })
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
    return google_search_all_results(
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
