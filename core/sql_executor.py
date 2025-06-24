import psycopg2

# def enforce_filters(sql: str) -> str:
#     filters = [
#         "age IS NOT NULL", "name IS NOT NULL", "department IS NOT NULL",
#         "height IS NOT NULL", "sugar IS NOT NULL",
#         "emp_data_master.corp_id = 'bbb269e5-b020-4257-ad8f-4da8c811801a'"
#     ]

#     if "FROM emp_data_master" in sql:
#         if "join org_employee_vitals_entity" not in sql.lower():
#             sql = sql.replace(
#                 "FROM emp_data_master",
#                 "FROM emp_data_master JOIN org_employee_vitals_entity ON emp_data_master.emp_id = org_employee_vitals_entity.emp_id"
#             )

#         if "WHERE" in sql.upper():
#             sql = sql.replace("WHERE", f"WHERE {' AND '.join(filters)} AND", 1)
#         else:
#             sql += f" WHERE {' AND '.join(filters)}"

#     return sql

# def run_query(sql: str, db_config: dict):
#     conn = psycopg2.connect(**db_config)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return result

# def enforce_filters(sql: str) -> str:
#     import re

#     # Extract alias used for emp_data_master (e.g., e)
#     match = re.search(r"from\s+emp_data_master\s+(as\s+)?(\w+)", sql, re.IGNORECASE)
#     alias = match.group(2) if match else "emp_data_master"  # fallback

#     # Add alias to applicable filters
#     filters = [
#     f"{alias}.age IS NOT NULL",
#     f"{alias}.name IS NOT NULL",
#     f"{alias}.department IS NOT NULL",
#     "v.height IS NOT NULL",     # ✅ Corrected
#     "v.sugar IS NOT NULL",
#     f"{alias}.corp_id = 'bbb269e5-b020-4257-ad8f-4da8c811801a'"
# ]


#     # Check if vitals table is already joined
#     if "join org_employee_vitals_entity" not in sql.lower():
#         sql = re.sub(
#             r"(from\s+emp_data_master\s+(as\s+)?\w+)",
#             r"\1 JOIN org_employee_vitals_entity v ON " + alias + ".emp_id = v.emp_id",
#             sql,
#             flags=re.IGNORECASE
#         )

#     # Add WHERE clause safely
#     filter_clause = " AND ".join(filters)
#     if re.search(r"\bWHERE\b", sql, re.IGNORECASE):
#         sql = re.sub(r"\bWHERE\b", f"WHERE {filter_clause} AND", sql, count=1, flags=re.IGNORECASE)
#     else:
#         sql += f" WHERE {filter_clause}"

#     return sql


# def run_query(sql: str, db_config: dict):
#     try:
#         conn = psycopg2.connect(**db_config)
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         result = cursor.fetchall()
#     except Exception as e:
#         print("Database query failed:", e)
#         result = []
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()
#     return result

import psycopg2

def enforce_filters(sql: str) -> str:
    filters = [
        "e.age IS NOT NULL", 
        "e.name IS NOT NULL", 
        "e.department IS NOT NULL",
        "v.height IS NOT NULL", 
        "v.sugar IS NOT NULL",
        "v.sugar <> ''",
        "e.corp_id = 'bbb269e5-b020-4257-ad8f-4da8c811801a'"
    ]

    alias = "e"
    join_table = "org_employee_vitals_entity"
    join_alias = "v"

    # Ensure FROM clause uses alias correctly
    if "FROM emp_data_master" in sql:
        sql = sql.replace("FROM emp_data_master", f"FROM emp_data_master {alias}")

    # Ensure JOIN clause is correctly formatted with alias
    if f"JOIN {join_table}" in sql and f"JOIN {join_table} {join_alias}" not in sql:
        sql = sql.replace(f"JOIN {join_table}", f"JOIN {join_table} {join_alias}")
    elif f"JOIN {join_table} {join_alias}" not in sql:
        sql = sql.replace(
            f"FROM emp_data_master {alias}",
            f"FROM emp_data_master {alias} JOIN {join_table} {join_alias} ON {alias}.emp_id = {join_alias}.emp_id"
        )

    # Add filters to WHERE clause
    filter_clause = " AND ".join(filters)
    if "WHERE" in sql.upper():
        sql = sql.replace("WHERE", f"WHERE {filter_clause} AND", 1)
    else:
        sql += f" WHERE {filter_clause}"

    return sql

def run_query(sql: str, db_config: dict):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print("Database query failed:", e)
        return []

if __name__ == "__main__":
    # Usage
    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'myPassword',
        'host': 'unotestdblatest.cs0v0vupxhfq.ap-south-1.rds.amazonaws.com',
        'port': 5432,
    }

    question = input("\n❓ Ask a question: ")
    # Simulate SQL generation (replace with actual generator call)
    sql = "SELECT e.name, v.sugar FROM emp_data_master e JOIN org_employee_vitals_entity v ON e.emp_id = v.emp_id ORDER BY v.sugar DESC LIMIT 5;"
    final_sql = enforce_filters(sql)

    print("\n🧠 Generated SQL:\n", final_sql)

    results = run_query(final_sql, db_config)
    print("\n📊 Results:")
    for row in results:
        print(row)




# ----------------------------------------------------------------------------------------------------
# import re

# def enforce_filters(sql: str) -> str:
#     # Replace fully qualified table names with aliases
#     sql = re.sub(r'\bemp_data_master\.', 'e.', sql)
#     sql = re.sub(r'\borg_employee_vitals_entity\.', 'v.', sql)

#     return sql

# import re

# def enforce_filters(sql: str) -> str:
#     # Ensure emp_data_master has alias 'e'
#     sql = re.sub(
#         r'FROM\s+emp_data_master(\s+|$)',
#         'FROM emp_data_master e ',
#         sql,
#         flags=re.IGNORECASE
#     )

#     # Ensure JOIN has alias 'v'
#     if 'JOIN org_employee_vitals_entity' in sql and ' v ' not in sql:
#         sql = re.sub(
#             r'JOIN\s+org_employee_vitals_entity(\s+ON)',
#             r'JOIN org_employee_vitals_entity v\1',
#             sql,
#             flags=re.IGNORECASE
#         )

#     # Fix column references
#     sql = re.sub(r'\bemp_data_master\.', 'e.', sql)
#     sql = re.sub(r'\borg_employee_vitals_entity\.', 'v.', sql)

#     # Enforced filters
#     filters = [
#         "e.age IS NOT NULL", "e.name IS NOT NULL", "e.department IS NOT NULL",
#         "v.height IS NOT NULL", "v.sugar IS NOT NULL",
#         "e.corp_id = 'bbb269e5-b020-4257-ad8f-4da8c811801a'"
#     ]
#     filter_clause = " AND ".join(filters)

#     if re.search(r'\bWHERE\b', sql, re.IGNORECASE):
#         sql = re.sub(r'\bWHERE\b', f"WHERE {filter_clause} AND", sql, count=1, flags=re.IGNORECASE)
#     else:
#         sql += f" WHERE {filter_clause}"

#     return sql

# import psycopg2
# from config.settings import DB_CONFIG

# def run_query(sql: str):
#     try:
#         conn = psycopg2.connect(
#             dbname=DB_CONFIG['dbname'],
#             user=DB_CONFIG['user'],
#             password=DB_CONFIG['password'],
#             host=DB_CONFIG['host'],
#             port=DB_CONFIG.get('port', 5432)
#         )
#         cur = conn.cursor()

#         cur.execute(sql)
#         rows = cur.fetchall()
#         columns = [desc[0] for desc in cur.description]
#         result = [dict(zip(columns, row)) for row in rows]

#         cur.close()
#         conn.close()
#         return result

#     except Exception as e:
#         return f"❌ Query Execution Failed:\n\n{str(e)}"




# import re

# def enforce_filters(sql_query: str) -> str:
#     # === Step 1: Normalize table aliases ===
#     # Ensure emp_data_master uses alias 'ed'
#     sql_query = re.sub(
#         r'\bFROM\s+emp_data_master\s+(?:AS\s+)?\w*', 
#         'FROM emp_data_master ed', 
#         sql_query, flags=re.IGNORECASE
#     )

#     # Ensure org_employee_vitals_entity uses alias 'oev'
#     sql_query = re.sub(
#         r'\bJOIN\s+org_employee_vitals_entity\s+(?:AS\s+)?\w*', 
#         'JOIN org_employee_vitals_entity oev', 
#         sql_query, flags=re.IGNORECASE
#     )

#     # === Step 2: Replace all incorrect alias usages ===
#     sql_query = sql_query.replace("e.", "ed.")
#     sql_query = sql_query.replace("v.", "oev.")

#     # === Step 3: Remove any FROM ed or JOIN oev — invalid replacements
#     sql_query = re.sub(r'\bFROM\s+ed\b', 'FROM emp_data_master ed', sql_query)
#     sql_query = re.sub(r'\bJOIN\s+oev\b', 'JOIN org_employee_vitals_entity oev', sql_query)

#     return sql_query.strip()
# import re

# def enforce_filters(sql_query: str) -> str:
#     # 1. Fix broken join (if JOIN keyword missing)
#     broken_join_pattern = re.search(
#         r"FROM\s+emp_data_master\s+(?:AS\s+)?(\w+)\s+org_employee_vitals_entity",
#         sql_query, re.IGNORECASE
#     )
#     if broken_join_pattern:
#         emp_alias = broken_join_pattern.group(1) or 'ed'
#         sql_query = re.sub(
#             r"FROM\s+emp_data_master\s+(?:AS\s+)?\w+\s+org_employee_vitals_entity",
#             f"FROM emp_data_master {emp_alias} JOIN org_employee_vitals_entity oev",
#             sql_query,
#             flags=re.IGNORECASE
#         )

#     # 2. Standardize aliases to ed and oev
#     sql_query = re.sub(r'\bFROM\s+emp_data_master\s+(?!ed\b)(\w+)?', 'FROM emp_data_master ed', sql_query, flags=re.IGNORECASE)
#     sql_query = re.sub(r'\bJOIN\s+org_employee_vitals_entity\s+(?!oev\b)(\w+)?', 'JOIN org_employee_vitals_entity oev', sql_query, flags=re.IGNORECASE)

#     # 3. Replace table references safely
#     sql_query = re.sub(r'\bemp_data_master\.', 'ed.', sql_query)
#     sql_query = re.sub(r'\borg_employee_vitals_entity\.', 'oev.', sql_query)

#     # 4. Fix any broken aliases like eoev → oev
#     sql_query = re.sub(r'\beoev\b', 'oev', sql_query)

#     return sql_query.strip()

# import re

# def enforce_filters(sql_query: str) -> str:
#     # Standardize aliases
#     sql_query = re.sub(r'\bemp_data_master\s+\w*', 'emp_data_master ed', sql_query)
#     sql_query = re.sub(r'\borg_employee_vitals_entity\s+\w*', 'org_employee_vitals_entity oev', sql_query)

#     # Ensure proper JOIN clause
#     if 'JOIN' not in sql_query.upper():
#         if 'FROM emp_data_master ed org_employee_vitals_entity oev' in sql_query:
#             sql_query = sql_query.replace(
#                 'FROM emp_data_master ed org_employee_vitals_entity oev',
#                 'FROM emp_data_master ed JOIN org_employee_vitals_entity oev ON ed.emp_id = oev.emp_id'
#             )

#     # Fix broken FROM clause if JOIN is missing
#     sql_query = re.sub(
#         r'FROM\s+emp_data_master\s+ed\s+org_employee_vitals_entity\s+oev',
#         'FROM emp_data_master ed JOIN org_employee_vitals_entity oev ON ed.emp_id = oev.emp_id',
#         sql_query,
#         flags=re.IGNORECASE
#     )

#     # Replace any wrong aliases
#     sql_query = sql_query.replace('e.', 'ed.')
#     sql_query = sql_query.replace('v.', 'oev.')

#     # Enforce required NOT NULL filters
#     filters = [
#         "ed.name IS NOT NULL",
#         "ed.age IS NOT NULL",
#         "ed.department IS NOT NULL",
#         "oev.height IS NOT NULL",
#         "oev.sugar IS NOT NULL"
#     ]
#     if 'WHERE' in sql_query.upper():
#         for condition in filters:
#             if condition not in sql_query:
#                 sql_query = re.sub(r'(WHERE\s+)', r'\1' + condition + ' AND ', sql_query, flags=re.IGNORECASE)
#     else:
#         sql_query += ' WHERE ' + ' AND '.join(filters)

#     return sql_query.strip()

# import re  (correct)

# def enforce_filters(sql_query: str) -> str:
#     # Correct table aliases to standard ones
#     sql_query = re.sub(r'\bemp_data_master\b\s*(\w+)?', 'emp_data_master ed', sql_query)
#     sql_query = re.sub(r'\borg_employee_vitals_entity\b\s*(\w+)?', 'org_employee_vitals_entity oev', sql_query)

#     # Ensure aliases are used consistently
#     sql_query = sql_query.replace('emp_data_master.', 'ed.')
#     sql_query = sql_query.replace('org_employee_vitals_entity.', 'oev.')
#     sql_query = sql_query.replace('eoev.', 'oev.')
#     sql_query = sql_query.replace('v.', 'oev.')
#     sql_query = sql_query.replace('e.', 'ed.')

#     # Add missing JOIN if not present
#     if 'JOIN org_employee_vitals_entity oev ON ed.emp_id = oev.emp_id' not in sql_query:
#         if 'FROM emp_data_master ed' in sql_query:
#             sql_query = sql_query.replace('FROM emp_data_master ed', 
#                 'FROM emp_data_master ed JOIN org_employee_vitals_entity oev ON ed.emp_id = oev.emp_id')

#     # Define required filters
#     required_filters = [
#         'ed.name IS NOT NULL',
#         'ed.age IS NOT NULL',
#         'ed.department IS NOT NULL',
#         'oev.sugar IS NOT NULL',
#         'oev.height IS NOT NULL',
#     ]

#     # Ensure WHERE clause exists
#     if 'WHERE' not in sql_query:
#         sql_query += ' WHERE ' + ' AND '.join(required_filters)
#     else:
#         where_clause = re.search(r'WHERE (.*?)(ORDER BY|LIMIT|$)', sql_query, re.IGNORECASE | re.DOTALL)
#         if where_clause:
#             current_filters = where_clause.group(1)
#             for f in required_filters:
#                 if f not in current_filters:
#                     sql_query = sql_query.replace('WHERE', f'WHERE {f} AND ', 1)

#     return sql_query

# import re

# def enforce_filters(sql: str) -> str:
#     # Clean up old malformed aliases (e.g., double joins, alias misplacement)
#     sql = re.sub(r'JOIN\s+org_employee_vitals_entity\s+oev.*?JOIN', 'JOIN', sql, flags=re.IGNORECASE | re.DOTALL)
    
#     # Normalize aliases
#     sql = re.sub(r'\bemp_data_master\b(?!\s+\w+)', 'emp_data_master ed', sql, flags=re.IGNORECASE)
#     sql = re.sub(r'\borg_employee_vitals_entity\b(?!\s+\w+)', 'org_employee_vitals_entity oev', sql, flags=re.IGNORECASE)

#     # Ensure proper JOIN clause
#     if 'JOIN org_employee_vitals_entity oev ON' not in sql:
#         sql = re.sub(
#             r'FROM\s+emp_data_master\s+ed',
#             'FROM emp_data_master ed JOIN org_employee_vitals_entity oev ON ed.emp_id = oev.emp_id',
#             sql,
#             flags=re.IGNORECASE
#         )

#     # Add necessary WHERE conditions if not already present
#     where_clause = re.search(r'\bWHERE\b(.*?)(ORDER BY|LIMIT|$)', sql, flags=re.IGNORECASE | re.DOTALL)
#     if where_clause:
#         conditions = where_clause.group(1).strip()
#         filters = [
#             'oev.sugar IS NOT NULL',
#             'oev.height IS NOT NULL',
#             'ed.department IS NOT NULL',
#             'ed.age IS NOT NULL',
#             'ed.name IS NOT NULL'
#         ]
#         for f in filters:
#             if f.lower() not in conditions.lower():
#                 conditions += f' AND {f}' if conditions else f
#         sql = re.sub(r'\bWHERE\b(.*?)(ORDER BY|LIMIT|$)',
#                      f'WHERE {conditions} \\2',
#                      sql, flags=re.IGNORECASE | re.DOTALL)
#     else:
#         # Add a new WHERE clause if not present
#         sql = re.sub(
#             r'(FROM\s+emp_data_master\s+ed\s+JOIN\s+org_employee_vitals_entity\s+oev\s+ON\s+ed\.emp_id\s+=\s+oev\.emp_id)',
#             r'\1 WHERE oev.sugar IS NOT NULL AND oev.height IS NOT NULL AND ed.department IS NOT NULL AND ed.age IS NOT NULL AND ed.name IS NOT NULL',
#             sql,
#             flags=re.IGNORECASE
#         )

#     return sql


# # generator.py

# import psycopg2
# # import re
# from config.settings import DB_CONFIG


# def run_query(sql: str):
#     try:
#         conn = psycopg2.connect(
#             dbname=DB_CONFIG['dbname'],
#             user=DB_CONFIG['user'],
#             password=DB_CONFIG['password'],
#             host=DB_CONFIG['host'],
#             port=DB_CONFIG.get('port', 5432)
#         )
#         cur = conn.cursor()

#         cur.execute(sql)
#         rows = cur.fetchall()
#         columns = [desc[0] for desc in cur.description]
#         result = [dict(zip(columns, row)) for row in rows]

#         cur.close()
#         conn.close()
#         return result

#     except Exception as e:
#         return f"❌ Query Execution Failed:\n\n{str(e)}"


# import re

# def enforce_filters(sql: str) -> str:
#     """
#     Enforces correct table aliasing and required filters for emp_data_master (alias e)
#     and org_employee_vitals_entity (alias v) in the SQL query.
#     """
#     # Remove incorrect alias patterns like "emp_data_master e AS e"
#     sql = re.sub(r'\bemp_data_master\s+e\s+AS\s+e\b', 'emp_data_master e', sql, flags=re.IGNORECASE)
#     sql = re.sub(r'\borg_employee_vitals_entity\s+v\s+AS\s+\w+\b', 'org_employee_vitals_entity v', sql, flags=re.IGNORECASE)

#     # Ensure correct aliases are used exactly once
#     sql = re.sub(r'\bemp_data_master\b(?!\s+e)', 'emp_data_master e', sql)
#     sql = re.sub(r'\borg_employee_vitals_entity\b(?!\s+v)', 'org_employee_vitals_entity v', sql)

#     # Normalize alias usage in WHERE clause and other parts
#     sql = re.sub(r'\b(ed|oev|eoev|oe|ov)\.', lambda m: 'e.' if 'name' in m.group(0) or 'department' in m.group(0) else 'v.', sql)

#     # Required data-quality filters
#     required_filters = [
#         'e.age IS NOT NULL',
#         'e.name IS NOT NULL',
#         'e.department IS NOT NULL',
#         'v.sugar IS NOT NULL',
#         'v.height IS NOT NULL'
#     ]

#     # Adjust or insert WHERE clause
#     where_match = re.search(r'\bWHERE\b', sql, re.IGNORECASE)
#     if where_match:
#         # Extract current filters
#         where_clause = sql[where_match.end():]
#         base_clause = where_clause.split("ORDER BY")[0].split("LIMIT")[0]
#         existing_filters = set(f.strip() for f in re.split(r'\s+AND\s+', base_clause) if f.strip())

#         # Add missing filters
#         missing_filters = [f for f in required_filters if f not in existing_filters]
#         combined_filters = " AND ".join(existing_filters.union(missing_filters))
#         sql = re.sub(r'(?i)\bWHERE\b\s+.*?(?=\bORDER\b|\bLIMIT\b|$)', f"WHERE {combined_filters} ", sql, flags=re.DOTALL)
#     else:
#         new_where = " AND ".join(required_filters)
#         if "ORDER BY" in sql:
#             parts = sql.split("ORDER BY")
#             sql = parts[0] + f" WHERE {new_where} ORDER BY" + parts[1]
#         elif "LIMIT" in sql:
#             parts = sql.split("LIMIT")
#             sql = parts[0] + f" WHERE {new_where} LIMIT" + parts[1]
#         else:
#             sql += f" WHERE {new_where}"

#     return sql
