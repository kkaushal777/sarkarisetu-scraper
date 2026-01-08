# SarkariSetu Scraper

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#)

Production-ready web scraper for **SarkariResult.com.cm** - Extracts Indian government job notifications, exam results, admit cards, and answer keys using Python, Ollama LLM normalization, and SQLite database.

## 🎯 Features

- **Two-Level Architecture**: Aggregator lists (job listings, results, admit cards) + Detail page scraping (recruitment, results, exam details)
- **Ollama LLM Integration**: Uses local LLM for intelligent data normalization and structured output
- **SQLite/PostgreSQL Support**: Built-in ORM layer for persistent storage
- **Robust Error Handling**: Automatic retries, fallback strategies, and comprehensive logging
- **Rate Limiting & Respect**: Configurable delays and concurrent job limits
- **CLI & Scheduler**: APScheduler integration for automated recurring scrapes
- **Comprehensive Testing**: Unit and integration tests included

## 📋 Project Structure

```
sarkarisetu/
├── config.py                 # Configuration management
├── models.py                 # Data models (Recruitment, Result, etc.)
├── exceptions.py             # Custom exceptions
├── scrapers/
│   ├── base.py              # Base scraper class
│   ├── aggregator.py        # Aggregator list scraper (jobs, results, etc.)
│   ├── recruitment.py       # Recruitment detail scraper
│   ├── result.py            # Result detail scraper
│   └── extract.py           # Content extraction utilities
├── normalizers/
│   ├── ollama_normalizer.py # Ollama LLM integration
│   ├── date_parser.py       # Indian date parsing
│   └── text_cleaner.py      # Text normalization
├── database/
│   ├── models.py            # SQLAlchemy models
│   ├── client.py            # Database operations
│   └── queries.py           # Query builders
├── scheduler/
│   ├── scheduler.py         # APScheduler setup
│   └── jobs.py              # Scheduled job definitions
├── cli/
│   └── main.py              # Click CLI interface
├── utils/
│   ├── logger.py            # Logging configuration
│   ├── cache.py             # Caching utilities
│   └── validators.py        # Data validators
├── tests/
│   ├── test_aggregator.py   # Aggregator tests
│   ├── test_recruitment.py  # Recruitment scraper tests
│   └── fixtures.py          # Test fixtures
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Ollama (optional, for LLM normalization)
- PostgreSQL or SQLite

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/sarkarisetu-scraper.git
cd sarkarisetu-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### Environment Variables

```bash
# .env file
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1

DATABASE_URL=sqlite:///sarkarisetu.db
# OR PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/sarkarisetu

LOG_LEVEL=INFO
LOG_FILE=logs/sarkarisetu.log
```

## 📖 Usage

### 1. Scrape Aggregator Lists (Jobs, Results, Admit Cards)

```python
from sarkarisetu.scrapers.aggregator import AggregatorScraper

# Scrape latest jobs
scraper = AggregatorScraper("https://sarkariresult.com.cm/latest-jobs/")
record = scraper.scrape()

print(f"Found {len(record.items)} jobs")
for item in record.items[:5]:
    print(f"{item.title} - Deadline: {item.metadata_value}")

# Save to JSON
with open("jobs.json", "w") as f:
    f.write(record.to_json())
```

### 2. Scrape Recruitment Details

```python
from sarkarisetu.scrapers.recruitment import RecruitmentScraper

scraper = RecruitmentScraper(
    "https://sarkariresult.com.cm/up-police-constable-recruitment-2026/"
)
detail = scraper.scrape()

print(f"Organization: {detail.organization}")
print(f"Total Posts: {detail.total_posts}")
print(f"Vacancies: {len(detail.vacancies)}")
for vacancy in detail.vacancies:
    print(f"  - {vacancy.post_name}: {vacancy.count}")
```

### 3. Use CLI

```bash
# Scrape latest jobs
python -m sarkarisetu.cli scrape-aggregator https://sarkariresult.com.cm/latest-jobs/ --output jobs.json

# Scrape with database storage
python -m sarkarisetu.cli scrape-aggregator https://sarkariresult.com.cm/latest-jobs/ --save-to-db

# Start scheduler for recurring scrapes
python -m sarkarisetu.cli schedule-jobs

# Query database
python -m sarkarisetu.cli list-jobs --limit 10
```

## 🔌 Ollama Integration

Optional LLM-powered data normalization:

```python
from sarkarisetu.normalizers.ollama_normalizer import OllamaNormalizer
from sarkarisetu.models import RecruitmentDetail

normalizer = OllamaNormalizer()
raw_detail = RecruitmentDetail(...)

# Normalize with LLM
normalized = normalizer.normalize_recruitment(raw_detail)
print(normalized.to_json())
```

## 🗄️ Database Usage

```python
from sarkarisetu.database.client import DatabaseClient
from sarkarisetu.config import config

db = DatabaseClient(config.db_url)

# Insert job listing
db.insert_aggregator_record(record)

# Query
jobs = db.query_jobs(organization="UP Police", limit=10)
for job in jobs:
    print(job.title, job.metadata_value)

# Update
db.update_item_status(item_id=1, status="closed")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_aggregator.py -v

# With coverage
pytest --cov=sarkarisetu tests/
```

## 📊 Data Models

### AggregatorRecord
- Page type (jobs, results, admit cards, answer keys)
- Source URL and fetch timestamp
- HTTP status code
- List of AggregatorItems with metadata (deadline, status)

### RecruitmentDetail
- Organization name and advertisement number
- Vacancies (post-wise breakdown)
- Important dates (application start/end, exam date)
- Application fees by category
- Age limits and eligibility criteria
- Selection process and useful links

### Other Models
- `ResultDetail`: Exam results, answer keys, merit lists
- `ExamCityDetails`: Exam city information, admit card status
- `AnswerKeyDetail`: Answer key PDFs and links

## 🔄 Pagination & Infinite Scroll

The scraper handles:
- Multi-page pagination
- Infinite scroll detection
- Content loading via JavaScript
- Dynamic content updates

## ⚠️ Rate Limiting & Ethics

- Respects `robots.txt`
- Configurable request delays (default: 5 seconds between requests)
- Concurrent job limits (default: 3)
- User-Agent headers identify the scraper
- ETag and Last-Modified header support

## 🛠️ Configuration

All settings in `sarkarisetu/config.py`:

```python
config = ScraperConfig(
    base_url="https://sarkariresult.com.cm",
    timeout=30,
    max_retries=3,
    concurrent_jobs=3,
    ollama_enabled=True,
    db_url="sqlite:///sarkarisetu.db"
)
```

## 📝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- SarkariResult.com.cm for the data
- selectolax for fast HTML parsing
- httpx for async HTTP client
- Ollama for local LLM support
- APScheduler for job scheduling

## ⚡ Performance Notes

- **HTML Parsing**: selectolax (Cython-based) is ~10x faster than BeautifulSoup
- **Concurrent Requests**: Uses asyncio for I/O-bound operations
- **Database**: Batch inserts for better throughput
- **Caching**: ETags and timestamps reduce unnecessary re-fetches

## 🐛 Issues & Support

Report bugs or request features via [GitHub Issues](https://github.com/yourusername/sarkarisetu-scraper/issues)

## 📚 Related Projects

- [SarkariSetu](https://github.com/yourusername/sarkarisetu) - Frontend aggregator
- [Gov-Job-Tracker](https://github.com/yourname/gov-job-tracker) - Notification system

---

**Last Updated**: January 2026
**Maintained by**: [Your Name](https://github.com/yourusername)
