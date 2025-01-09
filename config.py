import os

class NormalConfig:
    """Normal (Development/Production) configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:mysecretpassword@localhost/normal_dbname')

class TestConfig:
    """Test configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'test_secret_key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:mysecretpassword@postgres_test:5432/test_dbname')
    TESTING = True  # Enable testing mode in Flask
