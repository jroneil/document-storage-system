
# Document AI Agent

The **Document AI Agent** is a Flask-based application that automatically extracts keywords, generates tags, and enriches metadata for uploaded documents. It supports multiple file formats (PDF, Word, and plain text) and provides advanced features like summarization and sentiment analysis. Additionally, it includes **OCR (Optical Character Recognition)** support for scanned PDFs.

A **separate folder-scanning agent** is provided to periodically monitor a folder for new documents and upload them to the Document AI Agent via its API.

## RabbitMQ Integration

The **Document AI Agent** publishes messages to RabbitMQ whenever new documents are processed and inserted into the database. Other services can subscribe to these messages to react to new data in real time.

### RabbitMQ Configuration
- **Host**: `localhost`
- **Port**: `5672`
- **Queue**: `document_updates`
- **Username**: `guest`
- **Password**: `guest`

### Example Message
```
{
    "filename": "example.pdf",
    "tags": "AI,Machine Learning",
    "keywords": "artificial intelligence,deep learning",
    "summary": "This document discusses the impact of AI on modern technology...",
    "sentiment": "Sentiment(polarity=0.8, subjectivity=0.6)"
}
```
---

## Features

- **Document Upload**: Accepts PDF, Word, and plain text files.
- **Keyword Extraction**: Uses `KeyBERT` for context-aware keyword extraction.
- **Automated Tagging**: Generates tags using TF-IDF and K-Means clustering.
- **Metadata Enrichment**:
  - **Summarization**: Generates a concise summary of the document.
  - **Sentiment Analysis**: Analyzes the sentiment of the document.
- **OCR Support**: Extracts text from scanned PDFs using Tesseract OCR.
- **Folder Scanning**: A separate agent monitors a folder for new documents and uploads them automatically.
- **Database Integration**: Stores metadata in an SQLite database.
- **Search Functionality**: Allows searching documents by keywords or tags.

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (for scanned PDFs)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/document-ai-agent.git
   cd document-ai-agent
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies for the Document AI Agent**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install dependencies for the folder scanner**:
   ```bash
   pip install -r folder_scanner/requirements.txt
   ```

5. **Install Tesseract OCR**:
   - **Linux**:
     ```bash
     sudo apt install tesseract-ocr
     ```
   - **macOS**:
     ```bash
     brew install tesseract
     ```
   - **Windows**:
     - Download the Tesseract installer from [here](https://github.com/tesseract-ocr/tesseract).
     - Add the Tesseract installation path to your system's `PATH` environment variable.

6. **Set up the database**:
   - The SQLite database will be automatically created in the `instance/` folder when you run the application for the first time.

7. **Create the Scan Folder**:
   - Create a folder named `scan_folder` in the root directory of the project. This folder will be monitored for new documents.

---

## Usage

### Running the Document AI Agent
1. Start the Document AI Agent:
   ```bash
   python run.py
   ```

2. The application will be available at `http://localhost:5000`.

### Running the Folder Scanner
1. Start the folder scanner:
   ```bash
   python run_scanner.py
   ```

2. The folder scanner will monitor the `scan_folder` directory for new documents and upload them to the Document AI Agent every 5 minutes.

### Manual Document Upload
- Use the `/upload` endpoint to upload documents manually:
  ```bash
  curl -X POST -F "file=@example.pdf" http://localhost:5000/upload
  ```

### Search Documents
- Use the `/search` endpoint to search for documents by keywords or tags:
  ```bash
  curl http://localhost:5000/search?query=AI
  ```

---

## Project Structure

```
document_ai_agent/
│
├── app/                   # Existing Document AI Agent
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── utils.py
│   └── config.py
│
├── folder_scanner/        # New folder for the separate agent
│   ├── __init__.py
│   ├── scanner.py         # Folder scanning logic
│   └── requirements.txt   # Dependencies for the folder scanner
│
├── uploads/               # Folder for uploaded documents
├── scan_folder/           # Folder to monitor for new documents
├── instance/              # Folder for SQLite database
│   └── metadata.db
├── requirements.txt       # Dependencies for the Document AI Agent
├── run.py                 # Entry point for the Document AI Agent
├── run_scanner.py         # Entry point for the folder scanner
└── README.md              # Updated with folder-scanning agent
```

---

## Configuration

The application can be configured using the `config.py` file. Key settings include:

- `UPLOAD_FOLDER`: Folder to store uploaded documents.
- `SCAN_FOLDER`: Folder to monitor for new documents.
- `DATABASE_URI`: SQLite database URI.
- `SECRET_KEY`: Secret key for Flask sessions.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Flask**: Micro web framework for Python.
- **KeyBERT**: Keyword extraction using BERT embeddings.
- **Sumy**: Text summarization library.
- **TextBlob**: Sentiment analysis library.
- **Tesseract OCR**: Optical Character Recognition engine.

---

## Contact

For questions or feedback, please contact:
- **Your Name**  
- **Email**: your.email@example.com  
- **GitHub**: [your-username](https://github.com/your-username)

---
```

---

### Running the Project

1. **Start the Document AI Agent**:
   ```bash
   python run.py
   ```

2. **Start the Folder Scanner**:
   ```bash
   python run_scanner.py
   ```

3. **Add Documents to the Scan Folder**:
   - Place new documents (PDF, Word, or plain text) in the `scan_folder` directory.
   - The folder scanner will automatically upload them to the Document AI Agent every 5 minutes.

4. **Test the API**:
   - Upload documents manually using the `/upload` endpoint.
   - Search for documents using the `/search` endpoint.

---

This implementation provides a **separate folder-scanning agent** that works alongside the **Document AI Agent**. Let me know if you need further assistance!
