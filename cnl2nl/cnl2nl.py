import os
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def compile_prompt(prefix="Explain in everyday language what the following sentence says, improving the writing "
                          "style:\n", suffix="\nLimit your answer to 500 characters."):
    """
    Helper method to compile a prompt with both fixed prefix and suffix
    :param prefix:
    :param suffix:
    :return:
    """

    def _inner(cnl):
        prompt_template = prefix + cnl + suffix
        return prompt_template

    return _inner


def make_request_to_service(service_url=OLLAMA_URL, data=None):
    response = requests.post(service_url, data=data, headers={"Content-Type": "application/json"})
    return json.loads(response.text)


def contact_ollama_service(model='openchat', prompt=None):
    json_response = make_request_to_service(data=json.dumps({"model": model, "prompt": prompt, "stream": False}))
    return json_response['response']


def contact_openai_service(prompt, model="gpt-3.5-turbo"):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )
    except:
        return "NO OPENAI_API_KEY"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0, )
    return response.choices[0].message["content"]


def contact_llm_service(model='openchat', prompt=None):
    if model == 'openai':
        contact_openai_service(prompt)
    else:
        contact_ollama_service(model=model, prompt=None)
