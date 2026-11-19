# Tokeniser Embedding Playground

This is a minimal **Vercel**‑friendly project that provides a tiny web playground for:

1. **Tokenising** a piece of text (using HuggingFace `tokenizers`).
2. **Generating an embedding** for the same text (using the lightweight `sentence‑transformers/all‑MiniLM‑L6‑v2` model).

The project is deliberately lightweight so it stays well within Vercel's free tier limits.

---
## Tech stack
- **Python 3.11** (Vercel serverless functions support Python).
- **FastAPI** – tiny async web framework.
- **Uvicorn** – ASGI server (used only for local testing).
- **sentence‑transformers** – provides the embedding model.
- **tokenizers** – fast Rust‑based tokenizer (BPE for `bert-base-uncased`).

---
## Project structure
```
tokeniser/
├─ api/
│   └─ embed.py          # Vercel serverless function (FastAPI route)
├─ static/
│   └─ index.html        # Simple UI playground
├─ requirements.txt      # Python dependencies
├─ vercel.json           # Vercel configuration
└─ README.md             # You are reading it!
```

---
## How it works
- **`/api/embed`** (POST) receives JSON `{ "text": "your sentence" }`.
- The function:
  1. Uses the BERT tokenizer to return token IDs.
  2. Feeds the same text into the MiniLM model and returns a 384‑dimensional embedding.
- The frontend (`static/index.html`) lets you type text, calls the API, and displays the token list and a short preview of the embedding vector.

---
## Setup & local testing
```bash
# 1. Clone / create the folder (already here)
cd /Users/vedlad/Desktop/tokeniser

# 2. Create a virtual environment (optional but recommended)
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
uvicorn api.embed:app --reload
```
Open `http://127.0.0.1:8000/static/index.html` in a browser.

---
## Deploy to Vercel (free tier)
1. **Install Vercel CLI** (if you haven’t already):
   ```bash
   npm i -g vercel
   ```
2. **Login** (use a GitHub account – Vercel auth is free):
   ```bash
   vercel login
   ```
3. **Deploy** from the project root:
   ```bash
   vercel
   ```
   - Accept the defaults. Vercel will detect the `vercel.json` and create a Python serverless function.
   - When prompted for the framework, choose **Other**.
4. After the build finishes you’ll get a live URL like `https://tokeniser-xxxxx.vercel.app`.

---
## Staying within the free tier
- The MiniLM model (~57 MB) is cached on the first request and then reused – no repeated downloads.
- Each request runs in a serverless function with a **max execution time of 10 s** (default on Vercel free). The inference typically finishes in < 0.2 s.
- Bandwidth usage is tiny – only the small JSON payloads and the static HTML page.

---
## Next steps / optional improvements
- Add a simple **vector similarity demo** by storing generated vectors in memory and allowing a “search” against them.
- Replace the BERT tokenizer with a custom one if you need a different tokenisation scheme.
- Add a tiny README badge for Vercel deployment status.

---
## License
This example is MIT‑licensed – feel free to fork, modify, and deploy as you like.
