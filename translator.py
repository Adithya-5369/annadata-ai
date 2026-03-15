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
    "ta": "Tamil",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "or": "Odia",
    "en": "English",
}

LANG_CODES = {
    "hi": "hi-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "ta": "ta-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "or": "od-IN",
    "en": "en-IN",
}

# Unicode script ranges for detection
SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F),   # Devanagari
    "te": (0x0C00, 0x0C7F),   # Telugu
    "kn": (0x0C80, 0x0CFF),   # Kannada
    "ta": (0x0B80, 0x0BFF),   # Tamil
    "ml": (0x0D00, 0x0D7F),   # Malayalam
    "mr": (0x0900, 0x097F),   # Devanagari (same as Hindi)
    "bn": (0x0980, 0x09FF),   # Bengali
    "gu": (0x0A80, 0x0AFF),   # Gujarati
    "pa": (0x0A00, 0x0A7F),   # Gurmukhi
    "or": (0x0B00, 0x0B7F),   # Odia
}

def detect_language(text):
    try:
        total = len(text.strip())
        if total == 0:
            return "en"

        # Count script characters for each language
        scores = {}
        for lang, (start, end) in SCRIPT_RANGES.items():
            count = sum(1 for c in text if start <= ord(c) <= end)
            if count > 0:
                scores[lang] = count / total

        if scores:
            # Return language with highest script density
            best = max(scores, key=scores.get)
            if scores[best] > 0.08:
                return best

        # Fallback to langdetect
        lang = detect(text)
        return lang if lang in LANG_NAMES else "en"
    except:
        return "en"

def translate(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text
    try:
        # Split into chunks of 1800 chars if too long
        if len(text) > 1800:
            chunks = []
            words = text.split(". ")
            current = ""
            for sentence in words:
                if len(current) + len(sentence) < 1800:
                    current += sentence + ". "
                else:
                    chunks.append(current.strip())
                    current = sentence + ". "
            if current:
                chunks.append(current.strip())

            # Translate each chunk
            translated_chunks = []
            for chunk in chunks:
                if not chunk.strip():
                    continue
                result = _call_sarvam(chunk, src_lang, tgt_lang)
                translated_chunks.append(result)
            return "\n".join(translated_chunks)

        return _call_sarvam(text, src_lang, tgt_lang)

    except Exception as e:
        print(f"Translation error: {e}")
        return text

def _call_sarvam(text, src_lang, tgt_lang):
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
    translated = result.get("translated_text")
    if translated:
        return translated
    print(f"Sarvam error: {result}")
    return text

def to_english(text, src_lang):
    return translate(text, src_lang, "en")

def from_english(text, tgt_lang):
    return translate(text, "en", tgt_lang)