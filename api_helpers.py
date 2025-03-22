import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL, STABLE_HORDE_API_KEY, STABLE_HORDE_API_URL

def openrouter_chat_completion(messages, model="deepseek/deepseek-r1:free"):
    """Send a request to OpenRouter for chat completion."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return None

def stable_horde_image_generation(prompt):
    """Generate an image using Stable Horde API."""
    headers = {
        "apikey": STABLE_HORDE_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "params": {
            "n": 1,
            "width": 512,
            "height": 512,
            "steps": 20,
            "cfg_scale": 7.5,
            "sampler_name": "k_euler",
            "seed": "-1",
        },
        "nsfw": False,
        "trusted_workers": False,
        "models": ["stable_diffusion"],
        "censor_nsfw": False,
        "r2": True,
        "shared": False,
    }
    response = requests.post(STABLE_HORDE_API_URL, headers=headers, json=payload)
    if response.status_code == 202:
        return response.json().get("id")
    return None