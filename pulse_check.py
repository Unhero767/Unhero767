import sqlite3

def run_alignment():
    conn = sqlite3.connect('mlaos_manifold.db')
    cursor = conn.cursor()
    
    # Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temporal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            description TEXT,
            inertia_vector FLOAT DEFAULT 0.0
        );
    """)

    # Record Genesis (t=0)
    cursor.execute("INSERT INTO temporal_logs (event_type, description, inertia_vector) VALUES ('GENESIS', 'Alpha-Point established.', 0.0)")
    
    # Record Century One (t=1, I=0.0021)
    cursor.execute("INSERT INTO temporal_logs (event_type, description, inertia_vector) VALUES ('PULSE_01', 'Century One: First Quadratic Resistance.', 0.0021)")
    
    conn.commit()
    conn.close()
    print("[◦A] Alpha and Century One anchored in the Sanctuary.")

if __name__ == "__main__":
    run_alignment()
