from openai import OpenAI

def generate_sql(question: str, schema: str, api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    prompt = f"""
    It is a helpful assistant that translates natural language questions into SQL queries for PostgreSQL.
    Only use the tables 'emp_data_master' and 'org_employee_vitals_entity'.
    Columns:

    {schema}

    Use ILIKE for filtering names.
    Ignore rows where age, name, or hire_date is NULL.

    Question: "{question}"

    Respond only with the SQL query, no explanation.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip().strip("`").strip(";")
    return sql_query + ";"
