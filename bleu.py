from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk
nltk.download('punkt')

# Reference = expected translation
# Hypothesis = your model's output
reference = [["apply", "neem", "oil", "on", "the", "crop"]]
hypothesis = ["apply", "neem", "oil", "spray", "on", "crop"]

score = sentence_bleu(reference, hypothesis, smoothing_function=SmoothingFunction().method1)
print(f"BLEU Score: {score:.4f}")