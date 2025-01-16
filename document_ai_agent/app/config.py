import os

    
class Config:
    UPLOAD_FOLDER = 'uploads/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/metadata.db'
    SECRET_KEY = 'your_secret_key_here'
    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    RABBITMQ_QUEUE = 'document_updates'