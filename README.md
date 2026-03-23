# VibeGEO

An English-first Generative Engine Optimization (GEO) prototype built with Python + Streamlit.

## Features

- Input an `URL` or paste long English text
- Provide a target keyword/phrase
- Click `Start GEO Optimization`
- View `Original Content` vs `GEO-Optimized Content`
- See English keyword density + readability metrics (Flesch / Flesch-Kincaid)

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Code structure

- `vibeggeo/content_fetcher.py`: fetches and cleans text from URLs
- `vibeggeo/text_analyzer.py`: keyword density + readability scoring (English)
- `vibeggeo/optimizer.py`: English GEO rewrite engine (OpenAI + prompt with citations injection)
- `vibeggeo/geoprocess.py`: fetch -> analyze -> optimize pipeline
- `app.py`: Streamlit dashboard (English UI, two-column layout)
- `streamlit_app.py`: backward-compatible entrypoint that imports `app.py`

