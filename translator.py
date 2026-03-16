import os
import requests
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")
INDICTRANS_URL = "https://skitishly-idioplasmic-rex.ngrok-free.dev/translate"  # update each Colab restart

LANG_NAMES = {
    "hi": "Hindi", "te": "Telugu", "kn": "Kannada",
    "ta": "Tamil", "ml": "Malayalam", "mr": "Marathi",
    "bn": "Bengali", "gu": "Gujarati", "pa": "Punjabi",
    "or": "Odia", "en": "English",
}

LANG_CODES = {
    "hi": "hi-IN", "te": "te-IN", "kn": "kn-IN",
    "ta": "ta-IN", "ml": "ml-IN", "mr": "mr-IN",
    "bn": "bn-IN", "gu": "gu-IN", "pa": "pa-IN",
    "or": "od-IN", "en": "en-IN",
}

SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F),
    "te": (0x0C00, 0x0C7F),
    "kn": (0x0C80, 0x0CFF),
    "ta": (0x0B80, 0x0BFF),
    "ml": (0x0D00, 0x0D7F),
    "mr": (0x0900, 0x097F),
    "bn": (0x0980, 0x09FF),
    "gu": (0x0A80, 0x0AFF),
    "pa": (0x0A00, 0x0A7F),
    "or": (0x0B00, 0x0B7F),
}

def detect_language(text):
    try:
        total = len(text.strip())
        if total == 0:
            return "en"
        scores = {}
        for lang, (start, end) in SCRIPT_RANGES.items():
            count = sum(1 for c in text if start <= ord(c) <= end)
            if count > 0:
                scores[lang] = count / total
        if scores:
            best = max(scores, key=scores.get)
            if scores[best] > 0.08:
                return best
        lang = detect(text)
        return lang if lang in LANG_NAMES else "en"
    except:
        return "en"

# ── IndicTrans2 (Primary — Free, Best Quality) ──
def _indictrans_translate(text, src_lang, tgt_lang):
    try:
        # Split long text into sentences
        if len(text) > 500:
            sentences = text.split(". ")
            chunks = []
            current = ""
            for sent in sentences:
                if len(current) + len(sent) < 500:
                    current += sent + ". "
                else:
                    chunks.append(current.strip())
                    current = sent + ". "
            if current:
                chunks.append(current.strip())

            results = []
            for chunk in chunks:
                if not chunk.strip():
                    continue
                r = requests.post(
                    INDICTRANS_URL,
                    json={"text": chunk, "src_lang": src_lang, "tgt_lang": tgt_lang},
                    timeout=30
                )
                result = r.json().get("translated")
                if result:
                    results.append(result)
            if results:
                print(f"IndicTrans2 ✅ ({src_lang}→{tgt_lang})")
                return " ".join(results)
            return None

        # Short text — single call
        response = requests.post(
            INDICTRANS_URL,
            json={"text": text, "src_lang": src_lang, "tgt_lang": tgt_lang},
            timeout=30
        )
        result = response.json().get("translated")
        if result:
            print(f"IndicTrans2 ✅ ({src_lang}→{tgt_lang})")
            return result
    except Exception as e:
        print(f"IndicTrans2 unavailable: {e}")
    return None

# ── Sarvam (Fallback) ──
def _call_sarvam(text, src_lang, tgt_lang):
    try:
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
            print(f"Sarvam ✅ ({src_lang}→{tgt_lang})")
            return translated
        print(f"Sarvam error: {result}")
    except Exception as e:
        print(f"Sarvam error: {e}")
    return None

def _sarvam_translate(text, src_lang, tgt_lang):
    if len(text) > 1800:
        chunks = []
        current = ""
        for sentence in text.split(". "):
            if len(current) + len(sentence) < 1800:
                current += sentence + ". "
            else:
                chunks.append(current.strip())
                current = sentence + ". "
        if current:
            chunks.append(current.strip())
        return "\n".join([_call_sarvam(c, src_lang, tgt_lang) or c for c in chunks if c])
    return _call_sarvam(text, src_lang, tgt_lang)

def translate(text, src_lang, tgt_lang):
    if src_lang == tgt_lang:
        return text

    # Try IndicTrans2 first (free + best quality)
    result = _indictrans_translate(text, src_lang, tgt_lang)
    if result:
        return result

    # Fallback to Sarvam
    result = _sarvam_translate(text, src_lang, tgt_lang)
    if result:
        return result

    # Last resort — return original
    print("Both translators failed — returning original")
    return text

def to_english(text, src_lang):
    return translate(text, src_lang, "en")

def from_english(text, tgt_lang):
    return translate(text, "en", tgt_lang)