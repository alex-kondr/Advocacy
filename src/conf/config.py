from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url_advocacy: str = 'postgresql+psycopg2://user:password@localhost:5432/postgres'
    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 12345678
    cloudinary_api_secret: str = 'api_secret'
    secret_key: str = "ababagalamaga"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = "pass"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
