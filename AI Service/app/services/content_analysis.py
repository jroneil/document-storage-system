from transformers import pipeline

def analyze_content(text: str):
    try:
        classifier = pipeline("sentiment-analysis")
        result = classifier(text)
        return result
    except Exception as e:
        raise Exception(f"Failed to analyze content: {str(e)}")