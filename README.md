# Character & Species API

A GraphQL API (Flask + Ariadne) and Streamlit frontend for managing character and species data, backed by MongoDB.

## Features

- GraphQL API built with [Ariadne](https://ariadnegraphql.org/) and Flask
- Streamlit frontend for interacting with the data
- MongoDB storage via PyMongo
- NLP-related API endpoints
- Data normalization utilities

## Tech Stack

- **Backend:** Flask, Ariadne (GraphQL)
- **Frontend:** Streamlit
- **Database:** MongoDB (PyMongo)
- **Language:** Python 3.13

## Project Structure

```
.
├── app_graphql.py         # GraphQL API (Ariadne + Flask)
├── app_streamlit.py       # Streamlit frontend
├── db.py                  # MongoDB connection setup
├── nlp_api.py              # NLP-related API logic
├── normalize_arrays.py     # Data normalization utilities
├── test_db.py              # DB connection test script
├── requirements.txt        # Python dependencies
├── .env.example             # Environment variable template
└── INSTRUCTIONS/            # Original assignment instructions (PDF)
```

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your own MongoDB connection string:
   ```
   MONGODB_URI=your_mongodb_connection_string_here
   ```

## Running the Project

**GraphQL API:**
```bash
python app_graphql.py
```

**Streamlit frontend:**
```bash
streamlit run app_streamlit.py
```

**Test the database connection:**
```bash
python test_db.py
```

## Environment Variables

| Variable      | Description                          |
|---------------|---------------------------------------|
| `MONGODB_URI` | Connection string for your MongoDB instance |

## License

This project was created as part of a programming assignment. Add a license here if you plan to share it publicly.
