import sqlite3
import pandas as pd

def test_all_sql_queries():
    conn = sqlite3.connect("data/retail_database.db")
    cursor = conn.cursor()

    with open("sql/02_analytics_queries.sql", "r") as f:
        sql_content = f.read()

    # Split by semicolon to execute queries individually
    raw_queries = [q.strip() for q in sql_content.split(";") if q.strip()]

    print("--- VERIFYING ALL SQL ANALYTICS QUERIES ---")
    query_count = 0
    for q in raw_queries:
        # Ignore pure comments
        lines = [line for line in q.split("\n") if not line.strip().startswith("--")]
        clean_q = "\n".join(lines).strip()
        if not clean_q:
            continue

        query_count += 1
        try:
            df_res = pd.read_sql_query(clean_q, conn)
            print(f"Query {query_count} Executed Successfully! Rows returned: {len(df_res)}")
            print(df_res.head(2))
            print("-" * 50)
        except Exception as e:
            print(f"Error executing Query {query_count}: {e}")

    conn.close()

if __name__ == "__main__":
    test_all_sql_queries()
