import os
import requests
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

LANG_NAMES = {
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "en": "English",
}

LANG_CODES = {
    "hi": "hi-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "en": "en-IN",
}

def detect_language(text):
    try:
        # Count script characters
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
        kannada_chars = sum(1 for c in text if '\u0C80' <= c <= '\u0CFF')

        total = len(text.strip())
        if total == 0:
            return "en"

        # If any Indian script chars found → detect that language
        if hindi_chars / total > 0.1:
            return "hi"
        if telugu_chars / total > 0.1:
            return "te"
        if kannada_chars / total > 0.1:
            return "kn"

        # Fallback to langdetect
        lang = detect(text)
        return lang if lang in LANG_NAMES else "en"
    except:
        return "en"

def translate(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text

    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "input": text,
        "source_language_code": LANG_CODES.get(src_lang, "en-IN"),
        "target_language_code": LANG_CODES.get(tgt_lang, "en-IN"),
        "model": "sarvam-translate:v1",
        "enable_preprocessing": True,
    }

    response = requests.post(
        "https://api.sarvam.ai/translate",
        json=payload,
        headers=headers
    )
    result = response.json()
    return result.get("translated_text", text)

def to_english(text, src_lang):
    return translate(text, src_lang, "en")

def from_english(text, tgt_lang):
    return translate(text, "en", tgt_lang)