import PyPDF2

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")