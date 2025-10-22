import psycopg2
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

def save_document_metadata(record_data: dict):
    """
    Saves a single document metadata record to PostgreSQL.
    Handles idempotency and insert/update logic.
    """
    connection = None
    cursor = None
    try:
        idempotency_key = record_data.get('idempotency_key')
        transaction_type = record_data.get('transaction_type', 'new')
        
        if not idempotency_key:
            logger.error("Idempotency key is missing from record data.")
            raise ValueError("Idempotency key is required.")

        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = connection.cursor()

        # 1. Check for idempotency
        cursor.execute("SELECT outcome FROM idempotency_keys WHERE idempotency_key = %s", (idempotency_key,))
        idempotency_result = cursor.fetchone()

        if idempotency_result:
            logger.info(f"Idempotency key {idempotency_key} already processed with outcome: {idempotency_result[0]}. Skipping.")
            return True # Already processed

        # 2. Prepare data for insert/update
        # Ensure all fields are present, defaulting to None if not
        brand = record_data.get('brand')
        business_unit = record_data.get('business_unit')
        document_title = record_data.get('document_title')
        revision = record_data.get('revision')
        bucket = record_data.get('bucket', 'documents')
        object_key = record_data.get('object_key')
        content_type = record_data.get('content_type')
        size_bytes = record_data.get('size_bytes')
        checksum = record_data.get('checksum')
        uploader_id = record_data.get('uploader_id')
        upload_timestamp = record_data.get('upload_timestamp', datetime.now())
        tags = json.dumps(record_data.get('tags')) if record_data.get('tags') else None
        description = record_data.get('description')
        category = record_data.get('category')
        division = record_data.get('division')
        document_type = record_data.get('document_type')
        region = record_data.get('region')
        country = record_data.get('country')
        languages = json.dumps(record_data.get('languages')) if record_data.get('languages') else None
        alternate_part_numbers = json.dumps(record_data.get('alternate_part_numbers')) if record_data.get('alternate_part_numbers') else None
        thumbnail_path = record_data.get('thumbnail_path')
        expiration_date = record_data.get('expiration_date')
        acl = json.dumps(record_data.get('acl')) if record_data.get('acl') else None
        
        # Ensure required fields for unique key are present
        if not all([brand, business_unit, document_title, revision]):
            logger.error(f"Missing required fields for unique key (brand, business_unit, document_title, revision) in record: {idempotency_key}")
            raise ValueError("Missing required fields for unique key.")

        if transaction_type == 'new':
            # 3. Check for existing record for "new" transaction type
            cursor.execute(
                "SELECT id FROM documents WHERE brand = %s AND business_unit = %s AND document_title = %s AND revision = %s",
                (brand, business_unit, document_title, revision)
            )
            existing_record = cursor.fetchone()

            if existing_record:
                logger.warning(f"Record with brand '{brand}', business_unit '{business_unit}', title '{document_title}', revision '{revision}' already exists. Sending to DLQ (simulated by raising error).")
                # In a real scenario, this message would be sent to a DLQ.
                # For now, we raise an error to prevent insertion and allow nack/requeue.
                raise Exception(f"Duplicate record for 'new' transaction: {brand}-{business_unit}-{document_title}-{revision}")

            # 4. Insert new record
            insert_query = """
            INSERT INTO documents (
                brand, business_unit, document_title, revision, bucket, object_key, content_type, size_bytes,
                checksum, uploader_id, upload_timestamp, tags, description, category, division, document_type,
                region, country, languages, alternate_part_numbers, thumbnail_path, expiration_date, acl,
                created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            current_time = datetime.now()
            cursor.execute(insert_query, (
                brand, business_unit, document_title, revision, bucket, object_key, content_type, size_bytes,
                checksum, uploader_id, upload_timestamp, tags, description, category, division, document_type,
                region, country, languages, alternate_part_numbers, thumbnail_path, expiration_date, acl,
                current_time, current_time
            ))
            logger.info(f"Inserted new document: {brand}-{business_unit}-{document_title}-{revision}")

        elif transaction_type == 'update':
            # 5. Update existing record
            update_query = """
            UPDATE documents SET
                bucket = %s, object_key = %s, content_type = %s, size_bytes = %s, checksum = %s,
                uploader_id = %s, upload_timestamp = %s, tags = %s, description = %s, category = %s,
                division = %s, document_type = %s, region = %s, country = %s, languages = %s,
                alternate_part_numbers = %s, thumbnail_path = %s, expiration_date = %s, acl = %s,
                updated_at = %s
            WHERE brand = %s AND business_unit = %s AND document_title = %s AND revision = %s
            """
            current_time = datetime.now()
            cursor.execute(update_query, (
                bucket, object_key, content_type, size_bytes, checksum, uploader_id, upload_timestamp,
                tags, description, category, division, document_type, region, country, languages,
                alternate_part_numbers, thumbnail_path, expiration_date, acl, current_time,
                brand, business_unit, document_title, revision
            ))
            
            if cursor.rowcount == 0:
                logger.warning(f"Update failed: No record found with brand '{brand}', business_unit '{business_unit}', title '{document_title}', revision '{revision}'.")
                # This could mean the record doesn't exist, or it's a logic error.
                # Depending on requirements, this might be an error or a no-op.
                # For now, we'll log it and proceed as if it was a successful (though no-op) update.
            else:
                logger.info(f"Updated document: {brand}-{business_unit}-{document_title}-{revision}")
        else:
            logger.error(f"Invalid transaction_type: {transaction_type}")
            raise ValueError(f"Invalid transaction_type: {transaction_type}")

        # 6. Record idempotency key
        cursor.execute(
            "INSERT INTO idempotency_keys (idempotency_key, processed_at, outcome) VALUES (%s, %s, %s)",
            (idempotency_key, datetime.now(), 'success')
        )

        connection.commit()
        logger.info(f"Successfully saved document metadata for idempotency_key: {idempotency_key}")
        return True

    except psycopg2.Error as db_err:
        logger.error(f"Database error for idempotency_key {idempotency_key}: {db_err}")
        if connection:
            connection.rollback()
        raise Exception(f"Database error: {db_err}")
    except Exception as e:
        logger.error(f"Failed to save document metadata for idempotency_key {idempotency_key}: {str(e)}")
        logger.error(f"Record data that failed: {json.dumps(record_data, indent=2, default=str)}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def delete_document_metadata(document_id: str):
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = connection.cursor()

        query = "DELETE FROM documents WHERE document_id = %s"
        cursor.execute(query, (document_id,))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        raise Exception(f"Failed to delete document metadata: {str(e)}")
