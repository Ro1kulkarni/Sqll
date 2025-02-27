import openai
import pandas as pd
import streamlit as st
import os

# Set your OpenAI API Key
openai.api_key = "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"  # Replace with your actual API key

def load_csv_schema(file):
    """Extract schema from an uploaded CSV file."""
    try:
        df = pd.read_csv(file)
        table_name = os.path.splitext(file.name)[0]  # Get filename without extension
        schema = {table_name: list(df.columns)}  # Use column names as schema
        return schema
    except Exception as e:
        st.error(f"⚠ Error loading CSV: {e}")
        return {}

def generate_sql_query(prompt, schema_info):
    """Generates SQL query dynamically based on the provided schema."""
    formatted_schema = "\n".join([f"- {table}: {', '.join(columns)}" for table, columns in schema_info.items()])

    system_message = f"""
    You are an SQL expert. The user will provide natural language queries, and you will generate SQL queries.
    Use the following database schema:

    {formatted_schema}
    Rules:
    - Use only the provided tables and columns.
    - Follow PostgreSQL syntax.
    - Do NOT generate anything other than SQL.
    """

    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Streamlit UI
st.title("📝 Natural Language to SQL Query Generator")
st.markdown("Upload a CSV file and generate SQL queries from natural language.")

uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    db_schema = load_csv_schema(uploaded_file)
    if db_schema:
        st.success("✅ Schema extracted successfully!")
        st.json(db_schema)
        
        user_prompt = st.text_area("💬 Enter your query:")
        if st.button("Generate SQL") and user_prompt:
            sql_query = generate_sql_query(user_prompt, db_schema)
            st.code(sql_query, language='sql')
