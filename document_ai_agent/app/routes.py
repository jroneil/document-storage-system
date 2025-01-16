from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from .models import Document
from .utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_keywords,
    generate_summary,
    analyze_sentiment,
    generate_tags
)
from . import app, db

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Extract text based on file type
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        text = file.read().decode('utf-8')

    # Extract keywords
    keywords = extract_keywords(text)

    # Generate tags
    tags = generate_tags(keywords)

    # Generate summary
    summary = generate_summary(text)

    # Analyze sentiment
    sentiment = analyze_sentiment(text)

    # Save metadata to the database
    document = Document(
        filename=filename,
        tags=",".join(tags),
        keywords=",".join(keywords),
        summary=summary,
        sentiment=sentiment
    )
    db.session.add(document)
    db.session.commit()

    # Return metadata
    metadata = {
        "filename": filename,
        "tags": tags,
        "keywords": keywords,
        "summary": summary,
        "sentiment": sentiment
    }
    return jsonify(metadata), 200

@app.route('/search', methods=['GET'])
def search_documents():
    query = request.args.get('query')
    documents = Document.query.filter(
        Document.keywords.contains(query) | Document.tags.contains(query)
    ).all()
    results = [{
        "filename": doc.filename,
        "tags": doc.tags,
        "keywords": doc.keywords,
        "summary": doc.summary,
        "sentiment": doc.sentiment
    } for doc in documents]
    return jsonify(results)