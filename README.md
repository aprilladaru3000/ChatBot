# AI Q&A Chatbot with Python

## Features
- Answers frequently asked questions (rule-based)
- Falls back to an AI model (Hugging Face Transformers) when FAQ doesn’t match
- Deployable with Flask as a simple web API

## Usage
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python -m app.main
   ```
3. Ask questions via POST to `/ask` endpoint with JSON `{ "question": "...", "context": "..." }`

## Endpoints
- `/` : Health check
- `/ask` : POST endpoint for Q&A

## FAQ
- Add or edit FAQs in `app/faq.py`
