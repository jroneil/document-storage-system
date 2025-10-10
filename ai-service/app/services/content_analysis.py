from transformers import pipeline
import torch

# Initialize the model once (lazy loading)
_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        # Explicitly use CPU device
        device = 0 if torch.cuda.is_available() else -1  # -1 means CPU
        _classifier = pipeline("sentiment-analysis", device=device)
    return _classifier

def analyze_content(text: str):
    try:
        classifier = get_classifier()
        result = classifier(text)
        return result
    except Exception as e:
        raise Exception(f"Failed to analyze content: {str(e)}")
