
import sqlite3
import os
from datetime import datetime

DATABASE_PATH = "data/machine_memory.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machine_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            reported_fault TEXT NOT NULL,
            technical_context TEXT,
            fault_analysis TEXT,
            maintenance_plan TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_incident(
    machine_id,
    reported_fault,
    technical_context,
    fault_analysis,
    maintenance_plan
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO machine_incidents (
            machine_id,
            reported_fault,
            technical_context,
            fault_analysis,
            maintenance_plan,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        machine_id,
        reported_fault,
        technical_context,
        fault_analysis,
        maintenance_plan,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_machine_history(machine_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM machine_incidents
        WHERE machine_id = ?
        ORDER BY id DESC
    """, (machine_id,))

    records = cursor.fetchall()
    connection.close()

    return records


def get_machine_context(machine_id, limit=5):
    """
    Prepare reusable machine-specific historical context.
    This is the CAG context preparation layer.
    """

    records = get_machine_history(machine_id)[:limit]

    if not records:
        return "No previous maintenance history available for this machine."

    context = []

    for record in records:

        context.append(f"""
Previous Incident:
Date: {record[6]}
Reported Fault: {record[2]}

Previous Technical Context:
{record[3]}

Previous Fault Analysis:
{record[4]}

Previous Maintenance Plan:
{record[5]}
""")

    return "\n".join(context)


if __name__ == "__main__":

    initialize_database()

    print("Machine Memory database initialized successfully!")
    print("Database location:", DATABASE_PATH)
