import sqlite3
import csv
import os

def export_table_to_csv(db_file, table_name, output_csv):
    """Export the specified table to a CSV file."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        # Fetch the column names
        col_names = [description[0] for description in cursor.description]

        # Write data to CSV
        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(col_names)
            csv_writer.writerows(rows)

        print(f"Table '{table_name}' successfully exported to '{output_csv}'")
    
    except sqlite3.Error as e:
        print(f"An error occurred while exporting table '{table_name}': {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    db_file = r'tests\testfiles\multiplesubmenus.db'  # Replace with your .db file path
    table_name = 'workorders'     # The specific table you want to export
    output_csv = f"{table_name}.csv"

    export_table_to_csv(db_file, table_name, output_csv)
