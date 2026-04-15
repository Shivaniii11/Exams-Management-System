import pandas as pd
import mysql.connector

# Read CSV
df = pd.read_csv("C:/30 days/Python-SQL/p19-online exam system/exam system/questions_dataset.csv")

# 🔥 FIX NaN values
df = df.fillna("")

# Ensure correct_option is integer
df['correct_option'] = df['correct_option'].replace("", 0).astype(int)

# Connect DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="exam_system"
)

cursor = conn.cursor()

# Insert
sql = """
INSERT INTO questions (subject, question, option1, option2, option3, correct_option)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    values = (
        row['subject'],
        row['question'],
        row['option1'],
        row['option2'],
        row['option3'],
        row['correct_option']
    )
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted successfully!")