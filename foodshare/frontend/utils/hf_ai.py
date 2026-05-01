"""HuggingFace Inference API helper — used by Streamlit frontend for direct AI calls."""
import requests
import json
import streamlit as st

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
HF_URL   = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

def get_hf_token():
    try:
        return st.secrets["huggingface"]["token"]
    except Exception:
        return ""

def hf_chat(system_prompt: str, user_message: str, max_tokens: int = 300) -> str:
    """Call HuggingFace Inference API with Mistral chat format."""
    token = get_hf_token()
    prompt = f"<s>[INST] {system_prompt}\n\nUser: {user_message} [/INST]"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens, "temperature": 0.4, "return_full_text": False}
    }
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(HF_URL, headers=headers, json=payload, timeout=30)
        data = r.json()
        if isinstance(data, list) and data[0].get("generated_text"):
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and data.get("error"):
            return f"⚠️ HuggingFace: {data['error']}"
        return str(data)
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

def hf_analyze_food_waste(listings_data: list) -> str:
    """Analyze food waste patterns from listings."""
    system = (
        "You are a food waste reduction expert AI. "
        "Analyze the provided food listing data and give a short 3-bullet insight "
        "about patterns, urgency, and recommendations. Be concise."
    )
    user = f"Analyze these food listings: {json.dumps(listings_data[:10])}"
    return hf_chat(system, user, max_tokens=250)

def hf_match_recommendation(listing: dict, user_profile: dict) -> str:
    """Get AI recommendation for a specific listing-user match."""
    system = (
        "You are a food donation matching AI. "
        "In 2 sentences, explain why this listing is or isn't a good match for this recipient. Be direct."
    )
    user = f"Listing: {json.dumps(listing)}\nRecipient: {json.dumps(user_profile)}"
    return hf_chat(system, user, max_tokens=150)

def hf_impact_summary(metrics: dict) -> str:
    """Generate a personalized impact summary."""
    system = (
        "You are an impact reporting AI for a global food waste reduction platform. "
        "Write 2 motivating sentences summarizing this donor's positive environmental impact."
    )
    user = f"Metrics: {json.dumps(metrics)}"
    return hf_chat(system, user, max_tokens=150)
