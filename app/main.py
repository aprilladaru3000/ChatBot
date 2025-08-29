from flask import Flask, request, jsonify
from transformers import pipeline
from .faq import get_faq_answer

app = Flask(__name__)

# Load Hugging Face Transformers pipeline (e.g., distilbert-base-uncased-distilled-squad)
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    # Try FAQ first
    answer = get_faq_answer(question)
    if answer is not None:
        return jsonify({'answer': answer, 'source': 'faq'})
    # Fallback to AI model
    context = data.get('context', 'This is a general context for the AI model.')
    ai_result = qa_pipeline({'question': question, 'context': context})
    # Ensure ai_result is a dict and contains 'answer'
    if isinstance(ai_result, dict) and 'answer' in ai_result:
        return jsonify({'answer': ai_result['answer'], 'source': 'ai'})
    else:
        return jsonify({'answer': 'Sorry, I could not find an answer.', 'source': 'ai'})

@app.route('/')
def index():
    return 'AI Q&A Chatbot API is running.'

if __name__ == '__main__':
    app.run(debug=True)
