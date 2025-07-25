# VisitorLens AI

A full-stack application that provides actionable insights about tourist destinations by analyzing visitor reviews using advanced NLP techniques: abstractive summarization, topic modeling, and sentiment analysis.

## Overview

VisitorLens AI helps travelers and tourism professionals understand what visitors really think about destinations by:

- **Sentiment Analysis**: Automatically categorizes reviews into positive and negative feedback
- **Topic Modeling**: Identifies key themes and discussion points in reviews
- **Smart Search**: Allows custom keyword-based searches through review data
- **Interactive Visualizations**: Presents insights through an intuitive dashboard

## Architecture

```
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── constants/      # LLM prompts and constants
│   │   ├── models/         # Data models and schemas
│   │   ├── routers/        # API route handlers
│   │   └── utils/          # Utility functions
│   └── data/               # Review datasets
├── frontend/               # React frontend application
├── evaluation/             # Model evaluation scripts
└── preprocess/            # Data preprocessing pipeline
```

## Features

### Backend (FastAPI)
- **ChromaDB Integration**: Vector database for semantic search capabilities
- **LLM-Powered Summaries**: Generates positive/negative review summaries
- **Topic Analysis**: Identifies and analyzes discussion themes
- **Redis Caching**: Improves response times for repeated queries
- **CORS Support**: Enables frontend-backend communication

### Frontend (React)
- **Interactive Dashboard**: Clean, responsive user interface
- **Real-time Search**: Instant feedback as you search
- **Topic Exploration**: Click-through topic analysis with detailed breakdowns
- **Sentiment Visualization**: Clear positive/negative sentiment indicators
- **Custom Search**: Keyword-based review analysis

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- ChromaDB (Vector database)
- Redis (Caching layer)
- Transformers/Scikit-learn (NLP models)
- Topic modeling libraries

**Frontend:**
- React 
- Modern CSS styling
- Fetch API for HTTP requests

##Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Create .env file with your settings
COLLECTION_NAME=tourist_reviews
DATA_PATH=./data/reviews.csv
ID_COLUMN=review_id
DOCUMENT_COL=review_text
ADDITIONAL_COL=rating
```

5. Start the backend server:
```bash
uvicorn main:app --host localhost --port 8003 --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Data Format

Your review dataset should be in CSV format with the following columns:
- `review_id`: Unique identifier for each review
- `review_text`: The actual review content
- `rating`: Numerical rating (1-5 scale recommended)

Example:
```csv
review_id,review_text,rating
1,"Amazing beach with crystal clear water!",5
2,"Too crowded during peak season",2
```

## API Endpoints

### ChromaDB Operations
- `GET /chroma/documents/{keyword}/` - Retrieve documents by keyword
- `GET /chroma/documents/distance/{keyword}` - Get documents within distance threshold
- `GET /chroma/documents/count` - Get total document count

### LLM Analysis
- `GET /llm/summary?keyword=` - Generate keyword-specific summary
- `GET /llm/good_summary` - Generate positive review summary
- `GET /llm/bad_summary` - Generate negative review summary

### Topic Analysis
- `GET /topics/analyze` - Comprehensive topic and sentiment analysis

### Health Check
- `GET /health_check` - Service health status

## Usage

1. **Load Your Data**: Place your review CSV file in the `backend/data/` directory
2. **Start Services**: Launch both backend and frontend servers
3. **Search Destinations**: Use the search bar to analyze specific tourist sites
4. **Explore Topics**: Click on identified topics to see detailed sentiment breakdowns
5. **Custom Analysis**: Use the custom search feature for keyword-specific insights

## Features in Detail

### Sentiment Analysis
The application automatically categorizes reviews into positive and negative sentiment, providing percentage breakdowns and sample comments for each category.

### Topic Modeling
Advanced NLP techniques identify key themes in reviews (e.g., "food quality", "staff friendliness", "cleanliness") with associated sentiment scores.

### Caching Strategy
Redis caching ensures fast response times by storing computed analysis results, reducing processing time for repeated queries.