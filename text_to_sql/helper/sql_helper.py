import os
import sqlite3



def execute_sql_query(sql, db):
    """
    Execute an SQL query on the specified SQLite database.

    Parameters:
    - sql (str): The SQL query to execute.
    - db (str): The path to the SQLite database file.

    Returns:
    - list: The results of the executed SQL query.
    """
    sql = sql.strip()
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    sql_response=cur.fetchall()
    conn.commit()
    conn.close()
    return sql_response


def extract_schema_info(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Extract schema name (assuming the first part of the database path as schema name)
    schema_name = db_path.split('/')[-1].split('.')[0]

    info = f"CREATE SCHEMA {schema_name};\n"

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]  # Keep the exact table name
        
        # Get the table schema
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = cursor.fetchall()

        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        foreign_keys = cursor.fetchall()

        # Generate CREATE TABLE statement
        info += f"CREATE TABLE {table_name} (\n"
        for col in columns:
            col_def = f"    {col[1]} {col[2]}"
            if col[5]:  # Check if column is a PRIMARY KEY
                col_def += " PRIMARY KEY"
            if col[3] == 0:  # Check if column is NOT NULL
                col_def += " NOT NULL"
            if col[4] is not None:  # Check for DEFAULT value
                col_def += f" DEFAULT {col[4]}"
            info += col_def + ",\n"

        # Add foreign key constraints
        for fk in foreign_keys:
            fk_def = f"    FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]})"
            info += fk_def + ",\n"
        
        info = info.rstrip(",\n") + "\n);\n"

    # Add ALTER TABLE statements for foreign key constraints if required
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        foreign_keys = cursor.fetchall()

        for fk in foreign_keys:
            info += (f"ALTER TABLE {table_name} ADD CONSTRAINT FK_{table_name}_{fk[3]} "
                     f"FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]});\n")
    
    # Close the connection
    conn.close()

    return info