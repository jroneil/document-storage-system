from . import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    tags = db.Column(db.String(200))
    keywords = db.Column(db.String(200))
    summary = db.Column(db.Text)
    sentiment = db.Column(db.String(50))

    def __repr__(self):
        return f"<Document {self.filename}>"