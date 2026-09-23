import os
import re
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT", "http://localhost:4000")

st.set_page_config(page_title="NL → GraphQL CRUD (IMDB)")
st.title("Natural Language → GraphQL CRUD (IMDB)")

st.markdown("""
You can perform:

- **Read**: "Show top 5 movies with rating > 8"
- **Create**: "Add a movie titled 'My Movie' with rating 8.7 and year 2025"
- **Update**: "Update movie with id insert movie id without double quotation to rating 9.0 and title 'Updated Movie'"
- **Delete**: "Delete movie with id insert movie id without double quotation"
""")

nl_input = st.text_area("Enter your request", height=150)

# ------------------- Helper Functions -------------------

def clean_gql_output(llm_text):
    if not llm_text:
        return ""
    return llm_text.replace("```graphql", "").replace("```", "").replace("`", "").strip()

def parse_read_nl(nl_text):
    limit = 5
    rating_gt = 0
    top_match = re.search(r"top\s+(\d+)", nl_text, re.IGNORECASE)
    if top_match:
        limit = int(top_match.group(1))
    rating_match = re.search(r"rating\s*[>]\s*(\d+(\.\d+)?)", nl_text)
    if rating_match:
        rating_gt = float(rating_match.group(1))
    return limit, rating_gt

def parse_fields(nl_text):
    fields = {}
    title_match = re.search(r"titled\s+'(.+?)'", nl_text)
    if title_match:
        fields["title"] = title_match.group(1)
    rating_match = re.search(r"rating\s+(\d+(\.\d+)?)", nl_text)
    if rating_match:
        fields["rating"] = float(rating_match.group(1))
    year_match = re.search(r"year\s+(\d{4})", nl_text)
    if year_match:
        fields["year"] = int(year_match.group(1))
    votes_match = re.search(r"votes\s+(\d+)", nl_text)
    if votes_match:
        fields["votes"] = int(votes_match.group(1))
    revenue_match = re.search(r"revenue\s+(\d+(\.\d+)?)", nl_text)
    if revenue_match:
        fields["revenue"] = float(revenue_match.group(1))
    return fields

def gql_set_format(value):
    return f'"{value}"' if isinstance(value, str) else value

# ------------------- Run Button -------------------

if st.button("Run"):
    if not nl_input.strip():
        st.warning("Please enter a request.")
    else:
        nl_lower = nl_input.lower()
        if any(word in nl_lower for word in ["add", "create"]):
            operation = "create"
        elif "update" in nl_lower:
            operation = "update"
        elif "delete" in nl_lower:
            operation = "delete"
        else:
            operation = "read"

        gql_query = ""

        # ---------------- READ ----------------
        if operation == "read":
            limit, rating_gt = parse_read_nl(nl_input)
            gql_query = f"""
query {{
  movies(where: {{ rating_GT: {rating_gt} }}) {{
    ids
    title
    rating
    year
    votes
    revenue
  }}
}}
"""

        # ---------------- CREATE ----------------
        elif operation == "create":
            fields = parse_fields(nl_input)
            movie_id = str(uuid.uuid4())
            if fields:
                fields_str = ", ".join([f"{k}: {gql_set_format(v)}" for k, v in fields.items()])
                gql_query = f"""
mutation {{
  createMovies(input: [{{ ids: "{movie_id}", {fields_str} }}]) {{
    movies {{ ids title rating year votes revenue }}
  }}
}}
"""
            else:
                st.error("No valid fields found for creating a movie.")

        # ---------------- UPDATE ----------------
        elif operation == "update":
            id_match = re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", nl_input)
            movie_id = id_match.group(0) if id_match else ""
            fields = parse_fields(nl_input)
            if movie_id and fields:
                update_str = ", ".join([f"{k}: {{ set: {gql_set_format(v)} }}" for k, v in fields.items()])
                gql_query = f"""
mutation {{
  updateMovies(
    where: {{ ids: {{ eq: "{movie_id}" }} }},
    update: {{ {update_str} }}
  ) {{
    movies {{ ids title rating year votes revenue }}
  }}
}}
"""
            else:
                st.error("Cannot parse ID or fields for update.")

        # ---------------- DELETE ----------------
        elif operation == "delete":
            id_match = re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", nl_input)
            movie_id = id_match.group(0) if id_match else ""
            if movie_id:
                gql_query = f"""
mutation {{
  deleteMovies(
    where: {{ ids: {{ eq: "{movie_id}" }} }}
  ) {{
    nodesDeleted
  }}
}}
"""
            else:
                st.error("Cannot parse ID for delete.")

        # ---------------- Execute GraphQL ----------------
        if gql_query:
            st.subheader("Generated GraphQL")
            st.code(gql_query, language="graphql")
            try:
                gql_resp = requests.post(
                    GRAPHQL_ENDPOINT,
                    json={"query": clean_gql_output(gql_query)},
                    timeout=60
                )
                gql_resp.raise_for_status()
                data = gql_resp.json()
                if "errors" in data:
                    st.error("GraphQL Errors:")
                    st.json(data["errors"])
                else:
                    st.subheader("Response")
                    st.json(data)
                    if operation == "read":
                        movies = data.get("data", {}).get("movies", [])
                        limit, _ = parse_read_nl(nl_input)
                        movies_sorted = sorted(movies, key=lambda x: x.get("rating", 0), reverse=True)[:limit]
                        if movies_sorted:
                            st.subheader(f"Top {limit} Movies")
                            st.table(movies_sorted)
                        else:
                            st.warning("No movies returned.")
            except Exception as e:
                st.error(f"GraphQL execution failed: {e}")
