# 🌾 Annadata AI
### Multilingual + Code-Mixed Agricultural Advisory System

> *"Every Farmer. Every Phone. Every Language. Bringing AI to every Indian farmer, in their own language.* 🌾

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LLM](https://img.shields.io/badge/LLM-Sarvam--105B-green)
![Languages](https://img.shields.io/badge/Languages-10%2B%20Indian-orange)
![RAG](https://img.shields.io/badge/Pipeline-RAG%20%2B%20FAISS-brightgreen)
![BLEU](https://img.shields.io/badge/BLEU%20Score-0.2296-yellow)

---

## 📌 Overview

**Annadata AI** is an intelligent multilingual agricultural advisory system built for Indian farmers. It delivers expert-level farming guidance in **10+ Indian languages** including Hindi, Telugu, Kannada, Tamil, Malayalam, Marathi, Bengali, Gujarati, Punjabi, and Odia powered by **Sarvam-105B LLM** and a **Retrieval Augmented Generation (RAG)** pipeline grounded in verified ICAR documents and HuggingFace agriculture datasets.

A unique feature of Annadata AI is **code-mixed language support** where farmers can naturally type queries mixing their native language with English (e.g., *"मेरी wheat crop में yellow spots आ रहे हैं"*) and the system understands perfectly.

---

## 🎯 Problem Statement

India has **140M+ farmers** but:
- 70% cannot understand English but almost ICAR research is published in English
- Expert agricultural advice is inaccessible in villages (nearest KVK = 50+ km)
- Crop losses due to delayed pest/disease diagnosis
- Billions in govt subsidies unclaimed due to lack of scheme awareness
- Farmers exploited by middlemen due to lack of real-time market information

---

## ✅ Solution

Annadata AI bridges this gap by providing:
- Expert advice in farmer's **native language**
- **10 Indian languages** + English + Code-Mixed support
- Knowledge grounded in **verified ICAR documents**
- Available **24/7** via simple Gradio web interface

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🌱 Crop Advisory | Season & region-wise recommendations from ICAR |
| 🐛 Pest & Disease | Identify symptoms → get remedy instantly |
| 🌦️ Weather Alerts | Farming-specific weather guidance |
| 💰 Mandi Prices | Market price information |
| 🏛️ Govt Schemes | 25+ schemes: PM Kisan, PMFBY, KCC, PMKSY and more |
| 🪨 Soil Health | Fertilizer recommendations by crop & region |
| 🔀 Code-Mixed | Handles mixed Hindi+English, Telugu+English queries |

---

## 🗣️ Supported Languages

| Language | Script | Code |
|---|---|---|
| Hindi | हिंदी | hi-IN |
| Telugu | తెలుగు | te-IN |
| Kannada | ಕನ್ನಡ | kn-IN |
| Tamil | தமிழ் | ta-IN |
| Malayalam | മലയാളം | ml-IN |
| Marathi | मराठी | mr-IN |
| Bengali | বাংলা | bn-IN |
| Gujarati | ગુજરાતી | gu-IN |
| Punjabi | ਪੰਜਾਬੀ | pa-IN |
| Odia | ଓଡ଼ିଆ | od-IN |
| English | English | en-IN |

---

## 🏗️ System Architecture

```
Farmer Input (Any Indian Language / Code-Mixed)
        ↓
Unicode Script Detection + langdetect
        ↓
Sarvam Translate → English
        ↓
FAISS Semantic Search
(ICAR PDFs + KisanVaani + Crop Recommendation)
        ↓
Sarvam-105B LLM → Expert Answer
        ↓
Sarvam Translate → Farmer's Language
        ↓
Gradio UI Response
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Sarvam-105B (Free API) |
| Translation | Sarvam Translate v1 |
| Knowledge Base | ICAR PDFs + HuggingFace Datasets |
| Vector Database | FAISS |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| RAG Framework | LangChain |
| UI | Gradio |
| Language Detection | Unicode Script Analysis + langdetect |
| Backend | Python 3.10 |

---

## 📚 Knowledge Base

| Source | Type | Size |
|---|---|---|
| ICAR Official PDFs | Crop guides, pest management | 1,147 pages |
| PM Kisan Guidelines | Government scheme | 42 pages |
| Government Schemes TXT | 25+ schemes complete guide | 1 file |
| KisanVaani QA Dataset | Agriculture Q&A pairs | 2,000+ pairs |
| Crop Recommendation | N/P/K/soil/climate data | 2,200 records |
| **Total** | **Combined** | **~12,000+ chunks** |

---

## 📊 Performance

| Metric | Value |
|---|---|
| BLEU Score (Translation) | 0.2296 |
| Language Detection Accuracy | ~94% |
| Top-k Retrieval (k=4) | ~78% relevant |
| Avg Response Time | ~4.2 seconds |
| Languages Supported | 11 (10 Indian + English) |
| Knowledge Base Size | ~12,000+ chunks |

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/adithya-5369/annadata-ai
cd annadata-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API key to `.env`
```
SARVAM_API_KEY=your_key_here
```
Get free API key at: https://dashboard.sarvam.ai

### 5. Run
```bash
python app.py
```

Open: `http://127.0.0.1:7860`

---

## 💬 Example Queries

| Language | Query |
|---|---|
| Hindi | मेरी गेहूं की फसल में पीले धब्बे आ रहे हैं, क्या करूं? |
| Telugu | వరి పంటకు ఏ ఎరువులు వేయాలి? |
| Kannada | ಹತ್ತಿ ಬೆಳೆಗೆ ಕೀಟ ನಿರ್ವಹಣೆ ಹೇಗೆ? |
| Tamil | நெல் பயிருக்கு எந்த உரம் போட வேண்டும்? |
| Malayalam | നെൽകൃഷിക്ക് ഏത് വളം ഉപയോഗിക്കണം? |
| Code-Mixed | मेरी wheat crop में yellow spots आ रहे हैं |

---

## 📁 Project Structure

```
annadata-ai/
├── app.py              ← Main app + Gradio UI
├── rag_pipeline.py     ← PDF + Dataset loading + FAISS
├── translator.py       ← Sarvam translation + detection
├── llm_engine.py       ← Sarvam-105B answer generation
├── query_processor.py  ← Query classification + prompts
├── data/               ← ICAR PDFs
├── faiss_index/        ← Saved vector database
├── .env                ← API keys (not committed)
└── requirements.txt
```

---

## 🔮 Future Scope

- 🎤 Voice input in regional languages
- 📸 Crop image → AI disease diagnosis
- 📱 Offline mobile app for rural areas
- 🔗 PM Kisan portal direct integration
- 🌐 data.gov.in live mandi prices API
- 📡 IoT soil sensor integration

---

## Author

**Adithya Sai Srinivas**  
📧 muttaadithyasaisrinivas@gmail.com  
🌐 [Portfolio](https://adithya369.pages.dev) • [LinkedIn](https://linkedin.com/in/adithyasaisrinivas)

---

## 🛡 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this code with attribution.

---
