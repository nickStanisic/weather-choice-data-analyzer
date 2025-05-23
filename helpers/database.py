import os
import sqlalchemy
from google.cloud.sql.connector import Connector

def get_db_connection():
    """Get database connection - works for both local and Cloud SQL"""
    
    if os.getenv('ENVIRONMENT') == 'local':
        # For local testing with regular PostgreSQL
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME')}"
        return sqlalchemy.create_engine(connection_string)
    else:
        # For Cloud Run with Cloud SQL
        connector = Connector()
        
        def getconn():
            conn = connector.connect(
                os.getenv('CLOUD_SQL_CONNECTION_NAME'),  # e.g., "project:region:instance"
                "pg8000",
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db=os.getenv('DB_NAME'),
            )
            return conn
        
        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        return engine