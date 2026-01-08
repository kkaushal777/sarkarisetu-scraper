"""Configuration management for SarkariSetu scraper."""
import os
from dataclasses import dataclass, field
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ScraperConfig:
    """Main scraper configuration"""
    base_url: str = "https://sarkariresult.com.cm"
    timeout: int = 30
    user_agent: str = "SarkariSetuBot/1.0 (+contact: dev@sarkarisetu.com)"
    max_retries: int = 3
    retry_delay: int = 5
    concurrent_jobs: int = 3
    
    # Ollama settings
    ollama_enabled: bool = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # Database settings
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///sarkarisetu.db")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/sarkarisetu.log")


@dataclass
class AggregatorConfig:
    """Aggregator-specific configuration"""
    pages: Dict[str, str] = field(default_factory=lambda: {
        "latest_jobs": "https://sarkariresult.com.cm/latest-jobs/",
        "admit_card": "https://sarkariresult.com.cm/admit-card/",
        "result": "https://sarkariresult.com.cm/result/",
        "answer_key": "https://sarkariresult.com.cm/answer-key/"
    })
    max_items_per_page: int = 200


@dataclass
class OllamaConfig:
    """Ollama LLM configuration"""
    host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    temperature: float = 0.3
    top_p: float = 0.9
    num_predict: int = 500
    timeout: int = 60


# Global config instances
config = ScraperConfig()
aggregator_config = AggregatorConfig()
ollama_config = OllamaConfig()
