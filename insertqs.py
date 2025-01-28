import psycopg2

# Database connection details
DB_HOST = "129.232.211.166"  # Update with your DB host
DB_NAME = "events"  # Update with your DB name
DB_USER = "dylan"  # Update with your DB user
DB_PASSWORD = "super123duper"  # Update with your DB password

# Questions to insert
questions = [
    ("What is the capital of France?", "Paris"),
    ("What is 5 + 7?", "12"),
    ("Who wrote 'Romeo and Juliet'?", "Shakespeare"),
    ("What is the largest planet in our solar system?", "Jupiter"),
    ("What is the chemical symbol for water?", "H2O"),
]

# Connect to the database
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    # Insert questions into the database
    for question, answer in questions:
        cur.execute(
            "INSERT INTO questions (question, answer) VALUES (%s, %s);",
            (question, answer)
        )

    # Commit the transaction
    conn.commit()
    print("Questions inserted successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()
