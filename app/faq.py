# FAQ logic for rule-based answers

FAQS = {
    'what is your name?': 'I am an AI Q&A Chatbot.',
    'how does this work?': 'Ask a question. If it matches a FAQ, I answer directly. Otherwise, I use an AI model.'
    # Add more FAQs as needed
}

def get_faq_answer(question: str):
    q = question.strip().lower()
    return FAQS.get(q)
