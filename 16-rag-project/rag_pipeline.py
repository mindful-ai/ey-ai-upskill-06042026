
from retrieval import search
from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")

PROMPT = '''
Answer the medical question using the context.

Context:
{context}

Question:
{question}
'''

def ask(question):
    docs = search(question)
    prompt = PROMPT.format(context="\n".join(docs), question=question)
    return generator(prompt, max_length=200)
