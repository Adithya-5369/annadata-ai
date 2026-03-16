from flask import Flask, request, jsonify
import torch
from IndicTransToolkit.processor import IndicProcessor
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading IndicTrans2 on {device}...")

ip = IndicProcessor(inference=True)

print("Loading En→Indic model...")
en_indic_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-en-indic-1B", trust_remote_code=True)
en_indic_model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-en-indic-1B", trust_remote_code=True).to(device)

print("Loading Indic→En model...")
indic_en_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-indic-en-1B", trust_remote_code=True)
indic_en_model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-indic-en-1B", trust_remote_code=True).to(device)

print("IndicTrans2 ready! ✅")

INDICTRANS_CODES = {
    "hi": "hin_Deva", "te": "tel_Telu", "kn": "kan_Knda",
    "ta": "tam_Taml", "ml": "mal_Mlym", "mr": "mar_Deva",
    "bn": "ben_Beng", "gu": "guj_Gujr", "pa": "pan_Guru",
    "or": "ory_Orya", "en": "eng_Latn",
}

def run_translation(text, src_code, tgt_code, tokenizer, model):
    batch = ip.preprocess_batch([text], src_lang=src_code, tgt_lang=tgt_code)
    inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, max_length=256)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ip.postprocess_batch(decoded, lang=tgt_code)[0]

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data["text"]
    src = INDICTRANS_CODES.get(data["src_lang"], "eng_Latn")
    tgt = INDICTRANS_CODES.get(data["tgt_lang"], "hin_Deva")
    if data["src_lang"] == "en":
        result = run_translation(text, src, tgt, en_indic_tokenizer, en_indic_model)
    else:
        result = run_translation(text, src, tgt, indic_en_tokenizer, indic_en_model)
    return jsonify({"translated": result})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
