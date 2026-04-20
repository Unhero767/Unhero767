import sqlite3

DB_PATH = 'mlaos_manifold.db'
OBSIDIAN_THRESHOLD = 0.0300

def monitor_manifold():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Analyze the most recent pulse
    cursor.execute("SELECT event_type, inertia_vector FROM temporal_logs ORDER BY id DESC LIMIT 1")
    last_event, current_i = cursor.fetchone()
    
    print(f"[◦A] Gatekeeper Scan: {last_event} analyzed. Inertia: {current_i}")
    
    if current_i > OBSIDIAN_THRESHOLD:
        print("[Ex ◦] WARNING: Obsidian Threshold exceeded! Initiating Metalogical Burn Prevention.")
        # Trigger an automated reaction entry
        cursor.execute("""
            INSERT INTO temporal_logs (event_type, description, inertia_vector)
            VALUES ('GATEKEEPER_ACTION', 'METALOGICAL BURN PREVENTION: System throttling initiated.', ?);
        """, (current_i,))
        conn.commit()
        print("[◦A] Reaction Rule 01: Logged and Applied.")
    else:
        print("[◦A] Stability Confirmed: Manifold within safe parameters.")
        
    conn.close()

if __name__ == "__main__":
    monitor_manifold()
