# Mini Projects

A collection of fun mini projects to experiment with different technologies and ideas.

## Projects

### AI Trend Monitor

An intelligent agent that monitors the latest AI trends and implements basic versions of popular AI models and techniques.

#### Features

- Web scraping of AI news and research papers
- Trend analysis of AI topics
- Basic implementations of trending AI models
- REST API for accessing trend data and model implementations

#### Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration (see `.env.example`)

4. Run the application:
```bash
python main.py
```

#### Project Structure

- `src/`
  - `scraper/` - Web scraping modules
  - `analyzer/` - Trend analysis components
  - `models/` - Basic AI model implementations
  - `api/` - REST API endpoints
- `data/` - Stored data and model checkpoints
- `tests/` - Unit tests

## Contributing

Feel free to submit issues and enhancement requests!
