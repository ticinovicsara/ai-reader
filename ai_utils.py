import requests
from foundry_local import FoundryLocalManager
import json

alias = "phi-3.5-mini"
manager = FoundryLocalManager(alias)
model_info = manager.get_model_info(alias)

model_id = model_info.id
base_endpoint = manager.endpoint.rstrip('/')

def summarize(text: str) -> str:
    if len(text) > 2000:
        text = text[:2000] + "..."
    
    url = f"{base_endpoint}/chat/completions"
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly but formal AI assistant. Provide a concise summary in 200-300 characters."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.5,
        "max_tokens": 150
    }


    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, stream=True)
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def ask_question(text: str, question: str) -> str:
    if len(text) > 2000:
        text = text[:2000] + "..."
    
    url = f"{base_endpoint}/chat/completions"
    payload = {
        "model": model_id,
        "messages": [
        {
            "role": "system",
            "content": (
                "You are a friendly AI assistant. Answer questions using the document and general knowledge. "
                "Be concise, simple, and under 300 characters."
                "Answer the question. Use the document if the answer is there; if not, use your general knowledge. Indicate when you are using general knowledge."

            )
        },
        {
            "role": "user",
            "content": f"Document:\n{text}\n\nQuestion: {question}"
        }
    ],
        "temperature": 0.5,
        "max_tokens": 100
    }

    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
