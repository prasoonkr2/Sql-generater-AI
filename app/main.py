  
from core.sql_generator import generate_sql
from core.sql_executor import enforce_filters, run_query
from config.settings import OPENAI_API_KEY, DB_CONFIG

question = input("\n❓ Ask a question: ")

# Load schema summary
with open("schema/schema_summary.txt") as f:
    schema = f.read()

try:
    # Step 1: Generate SQL from the natural language question
    sql = generate_sql(question, schema, OPENAI_API_KEY)

    # Step 2: Enforce filters and joins
    sql = enforce_filters(sql)

    print("\n🧠 Generated SQL:\n", sql)

    # Step 3: Run the SQL query using correct db_config
    results = run_query(sql, DB_CONFIG)

    print("📊 Results:")
    for row in results:
        print(row)

except Exception as e:
    print("❌ Error:", e)
 






# from core.sql_generator import generate_sql
# from core.sql_executor import enforce_filters, run_query
# from config.settings import OPENAI_API_KEY, DB_CONFIG


# question = input("\n❓ Ask a question: ")

# # Load schema summary
# with open("schema/schema_summary.txt") as f:
#     schema = f.read()

# try:
#     # Step 1: Generate SQL from the natural language question
#     sql = generate_sql(question, schema, OPENAI_API_KEY)

#     # Step 2: Replace incorrect table references with aliases
#     sql = enforce_filters(sql)

#     print("\n🧠 Generated SQL:\n", sql)

#     # Step 3: Run the SQL query
#     #results = run_query(sql, DB_CONFIG)
#     results = run_query(sql)

#     print("📊 Results:")
#     for row in results:
#         print(row)

# except Exception as e:
#     print("❌ Error:", e)