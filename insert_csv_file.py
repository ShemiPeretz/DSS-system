import pandas as pd
import mysql.connector

# Load the Excel data
excel_file = "project_db.csv"
df = pd.read_csv(excel_file)
print(df)

# Convert 'Valid start time' and 'Transaction time' to the correct datetime format
df['Valid start time'] = pd.to_datetime(df['Valid start time'], format='%d/%m/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
df['Transaction time'] = pd.to_datetime(df['Transaction time'], format='%d/%m/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="q6rh3b",
    database="patient_data"
)

cursor = db_connection.cursor()

# Insert the data into the database
for idx, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO test_results (id, first_name, last_name, loinc_num, value, unit, valid_start_time, transaction_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            idx + 1,
            row['First name'],
            row['Last name'],
            row['LOINC-NUM'],
            row['Value'],
            row['Unit'],
            row['Valid start time'],
            row['Transaction time']
        )
    )

db_connection.commit()
cursor.close()
db_connection.close()

print("Data inserted successfully.")
