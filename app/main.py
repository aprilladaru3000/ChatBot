from flask import Flask, request, jsonify
from transformers import pipeline
from .faq import get_faq_answer
from .history import create_session, add_turn, get_history, clear_session, add_feedback
@app.route('/session/<session_id>/feedback', methods=['POST'])
def session_feedback(session_id):
    """
    Submit feedback for a specific turn in the session history.
    JSON body: {"turn_index": int, "feedback": str}
    """
    data = request.get_json() or {}
    turn_index = data.get('turn_index')
    feedback = data.get('feedback')
    if turn_index is None or feedback is None:
        return jsonify({'error': 'turn_index and feedback are required'}), 400
    ok = add_feedback(session_id, int(turn_index), feedback)
    if ok:
        return jsonify({'session_id': session_id, 'turn_index': turn_index, 'feedback': feedback, 'status': 'success'})
    else:
        return jsonify({'error': 'Invalid session_id or turn_index'}), 400

app = Flask(__name__)

# Initialize the QA pipeline lazily to avoid heavy initialization on import
_qa_pipeline = None

def get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
    return _qa_pipeline


@app.route('/session', methods=['POST'])
def new_session():
    session_id = create_session()
    return jsonify({'session_id': session_id})


@app.route('/session/<session_id>/history', methods=['GET'])
def session_history(session_id):
    history = get_history(session_id)
    return jsonify({'session_id': session_id, 'history': history})


@app.route('/session/<session_id>/clear', methods=['POST'])
def session_clear(session_id):
    ok = clear_session(session_id)
    return jsonify({'session_id': session_id, 'cleared': ok})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    session_id = data.get('session_id')

    if not question:
        return jsonify({'error': 'question is required'}), 400

    # Try FAQ first
    answer = get_faq_answer(question)
    if answer is not None:
        if session_id:
            add_turn(session_id, question, answer, 'faq')
        return jsonify({'answer': answer, 'source': 'faq'})

    # Fallback to AI model
    context = data.get('context', 'This is a general context for the AI model.')
    try:
        qa = get_qa_pipeline()
        ai_result = qa({'question': question, 'context': context})
    except Exception as e:
        return jsonify({'error': 'AI model error', 'details': str(e)}), 500

    if isinstance(ai_result, dict) and 'answer' in ai_result:
        answer_text = ai_result['answer']
    else:
        answer_text = 'Sorry, I could not find an answer.'

    if session_id:
        add_turn(session_id, question, answer_text, 'ai')

    return jsonify({'answer': answer_text, 'source': 'ai'})


@app.route('/')
def index():
    return 'AI Q&A Chatbot API is running.'


if __name__ == '__main__':
    app.run(debug=True)
