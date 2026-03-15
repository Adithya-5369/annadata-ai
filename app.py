import os
import gradio as gr
from dotenv import load_dotenv
from rag_pipeline import load_pdfs, build_knowledge_base, load_knowledge_base, get_relevant_context
from translator import detect_language, to_english, from_english, LANG_NAMES
from query_processor import classify_query, build_prompt
from llm_engine import generate_answer

load_dotenv()

# Load knowledge base
if os.path.exists("faiss_index"):
    print("Loading existing knowledge base... ✅")
    vectorstore = load_knowledge_base()
else:
    print("Building knowledge base...")
    docs = load_pdfs("data/")
    vectorstore = build_knowledge_base(docs)

print("🌾 Annadata AI ready!")

def process_query(user_input, selected_language):
    if not user_input.strip():
        return "Please enter a question."
    try:
        # Step 1: Detect language
        if selected_language == "Auto Detect":
            lang = detect_language(user_input)
        else:
            lang_map = {
                "Hindi": "hi",
                "Telugu": "te",
                "Kannada": "kn",
                "English": "en"
            }
            lang = lang_map[selected_language]

        print(f"\n--- New Query ---")
        print(f"Language: {LANG_NAMES.get(lang, 'English')}")
        print(f"Input: {user_input}")

        # Step 2: Translate to English
        english_query = to_english(user_input, lang)
        print(f"English: {english_query}")

        # Step 3: Classify + retrieve context
        category = classify_query(english_query)
        context = get_relevant_context(english_query, vectorstore)
        print(f"Category: {category}")

        # Step 4: Generate answer
        english_answer = generate_answer(english_query, context, category)
        print(f"Answer (EN): {english_answer}")

        # Step 5: Translate back
        final_answer = from_english(english_answer, lang)
        print(f"Final ({lang}): {final_answer[:100]}...")

        return final_answer

    except Exception as e:
        return f"Error: {str(e)}"

# Gradio UI
with gr.Blocks(title="Annadata AI 🌾") as demo:
    gr.Markdown("""
    # 🌾 Annadata AI
    ### Multilingual Agricultural Advisory — Hindi | Telugu | Kannada
    *Expert farming advice in your language, anytime.*
    """)

    with gr.Row():
        with gr.Column(scale=3):
            user_input = gr.Textbox(
                label="Your Question",
                placeholder="मेरी फसल में कीड़े लग रहे हैं... / మీ ప్రశ్న... / ನಿಮ್ಮ ಪ್ರಶ್ನೆ...",
                lines=3
            )
        with gr.Column(scale=1):
            language_selector = gr.Dropdown(
                choices=["Auto Detect", "Hindi", "Telugu", "Kannada", "English"],
                value="Auto Detect",
                label="Language / भाषा"
            )

    submit_btn = gr.Button("🌱 Get Advice", variant="primary", size="lg")
    output = gr.Textbox(label="Annadata AI Response", lines=8, interactive=False)

    gr.Examples(
        examples=[
            ["मेरी गेहूं की फसल में पीले धब्बे आ रहे हैं, क्या करूं?", "Hindi"],
            ["వరి పంటకు ఏ ఎరువులు వేయాలి?", "Telugu"],
            ["ಹತ್ತಿ ಬೆಳೆಗೆ ಕೀಟ ನಿರ್ವಹಣೆ ಹೇಗೆ?", "Kannada"],
            ["What is PM Kisan scheme and how to apply?", "English"],
            ["कपास की फसल में गुलाबी सुंडी कैसे रोकें?", "Hindi"],
        ],
        inputs=[user_input, language_selector]
    )

    submit_btn.click(
        fn=process_query,
        inputs=[user_input, language_selector],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True, theme=gr.themes.Soft())