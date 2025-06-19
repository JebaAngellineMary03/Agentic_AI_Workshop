from transformers import pipeline

def detect_ai_written(text):
    classifier = pipeline("text-classification", model="roberta-base-openai-detector")
    result = classifier(text[:512])
    return f"[Authorship Verifier] Prediction: {result[0]['label']} (Confidence: {result[0]['score']:.2f})"
