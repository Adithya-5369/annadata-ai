# 🌾 Annadata AI
### Multilingual + Code-Mixed Agricultural Advisory System

> "Every Farmer. Every Phone. Every Language."

## Overview
Annadata AI delivers expert farming guidance in **Hindi, Telugu, and Kannada**
powered by Sarvam-105B LLM and ICAR verified knowledge base via RAG pipeline.

## Features
- 🌱 Crop Advisory
- 🐛 Pest & Disease Detection
- 🌦️ Weather Alerts
- 💰 Mandi Prices
- 🏛️ Government Schemes
- 🪨 Soil Health Tips
- 🔀 Code-Mixed Language Support

## Tech Stack
| Component | Technology |
|---|---|
| LLM | Sarvam-105B (Free API) |
| Translation | Sarvam Translate |
| Knowledge Base | ICAR PDFs + FAISS |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| UI | Gradio |
| Backend | Python + LangChain |

## Setup
```bash
git clone https://github.com/adithya-5369/annadata-ai
cd annadata-ai
pip install -r requirements.txt
```

Add your API key to `.env`:
```
SARVAM_API_KEY=your_key_here
```

Run:
```bash
python app.py
```

## Architecture
```
Farmer Input (Hindi/Telugu/Kannada/Mixed)
        ↓ Language Detection
        ↓ Sarvam Translate → English
        ↓ FAISS Search (ICAR Knowledge Base)
        ↓ Sarvam-105B LLM
        ↓ Translate Back → Farmer's Language
        ↓ Gradio UI Response
```

## Languages Supported
- Hindi (हिंदी)
- Telugu (తెలుగు)  
- Kannada (ಕನ್ನಡ)
- English
- Code-Mixed (e.g. "मेरी wheat crop में yellow spots")

## NLP Minor Project — B.Tech CSE

## Author

**Adithya Sai Srinivas**  
📧 muttaadithyasaisrinivas@gmail.com  
🌐 [Portfolio](https://adithya369.pages.dev) • [LinkedIn](https://linkedin.com/in/adithyasaisrinivas)

---

## 🛡 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this code with attribution.

---
