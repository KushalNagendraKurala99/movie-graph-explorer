# Movie Graph Explorer

A GraphQL API over a Neo4j graph database of IMDB movie data, paired with a Streamlit frontend that lets users query the graph in natural language via a local Ollama LLM.

## Tech Stack

- **Backend:** Node.js, Apollo Server, `@neo4j/graphql`, Neo4j driver
- **Database:** Neo4j (graph database)
- **Frontend:** Python, Streamlit
- **LLM:** Ollama (local model for natural-language querying)
- **Data:** IMDB Movie Data (CSV, imported into Neo4j)

## Project Structure

```
.
├── backend/
│   ├── index.js            # GraphQL server (Apollo + Neo4jGraphQL)
│   ├── importCsv.js         # Imports IMDB-Movie-Data.csv into Neo4j
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── app.py               # Streamlit app
│   ├── requirements.txt
│   └── .env.example
├── IMDB-Movie-Data.csv       # Source dataset
└── INSTRUCTIONS/             # Original assignment instructions (PDF)
```

## Setup

### Backend (Node.js + Neo4j)

1. Install dependencies:
   ```bash
   cd backend
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your Neo4j connection details:
   ```
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password_here
   PORT=4000
   ```

3. Import the movie data into Neo4j:
   ```bash
   npm run import-csv
   ```

4. Start the GraphQL server:
   ```bash
   npm start
   ```

### Frontend (Python + Streamlit)

1. Create and activate a virtual environment:
   ```bash
   cd frontend
   python -m venv venv

   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   GRAPHQL_ENDPOINT=http://localhost:4000/graphql
   OLLAMA_API=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Environment Variables

**Backend**

| Variable         | Description                          |
|-------------------|---------------------------------------|
| `NEO4J_URI`        | Connection URI for your Neo4j instance |
| `NEO4J_USER`        | Neo4j username                        |
| `NEO4J_PASSWORD`    | Neo4j password                        |
| `PORT`              | Port for the GraphQL server           |

**Frontend**

| Variable            | Description                                |
|----------------------|----------------------------------------------|
| `GRAPHQL_ENDPOINT`    | URL of the backend GraphQL server            |
| `OLLAMA_API`          | URL of the local Ollama API                  |
| `OLLAMA_MODEL`        | Name of the Ollama model to use              |

## License

This project was created as part of a programming assignment. Add a license here if you plan to share it publicly.
