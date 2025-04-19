# Google Custom Search Web App

A simple web-based application for performing Google Custom Search queries via FastAPI backend and an HTML frontend.

## Features

- Use Google Custom Search API to retrieve web results
- Parameterized search (language, location, date, etc.)
- Export results to CSV via browser
- RESTful API with FastAPI

## Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/google-search-app.git
cd google-search-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file using `.env.example`:

```env
GOOGLE_API_KEY=your_api_key
SEARCH_ENGINE_ID=your_cse_id
```

### 4. Run the application

#### Backend (FastAPI):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend (static HTML):

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080/index.html`

## API Reference

- `GET /search`: perform search with parameters

Example query:

```
/search?search_terms=best+broker&user_location=us
```

## Deployment with Docker

_Coming soon in next step..._

