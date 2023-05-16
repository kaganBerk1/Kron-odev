import psycopg2
import csv

database = "kron"
user = "kron_support"
password = "Bau1234."
host = "192.168.1.102"
port = "5432"



def export_database(database, user, password, host, port):
    # Connect to the database
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema != 'pg_catalog' AND table_schema != 'information_schema';")
    tables = cursor.fetchall()

    # Export each table to a separate CSV file
    for schema, table_name in tables:
        file_name = f"{schema}_{table_name}.csv"

        # Fetch all rows from the table
        cursor.execute(f"SELECT * FROM \"{schema}\".\"{table_name}\";")
        rows = cursor.fetchall()

        # Get the column names
        column_names = [desc[0] for desc in cursor.description]

        # Write the rows to the CSV file
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(column_names)
            csv_writer.writerows(rows)

    # Close the database connection
    cursor.close()
    conn.close()

# Provide the database credentials

# Export the database
export_database(database, user, password, host, port)