import sqlite3
import math

DB_PATH = 'mlaos_manifold.db'
GOLDEN_PLUMB = 0.0042

def get_current_state():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Find the most recent pulse
    cursor.execute("SELECT COUNT(*) FROM temporal_logs WHERE event_type LIKE 'PULSE_%'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def execute_pulse(century):
    # Quadratic Inertia Formula: I = k * (t^2 / (1 + t))
    inertia = GOLDEN_PLUMB * (math.pow(century, 2) / (1 + century))
    inertia = round(inertia, 4)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO temporal_logs (event_type, description, inertia_vector)
            VALUES (?, ?, ?);
        """, (f'PULSE_{century:02}', f'Century {century} automated pulse.', inertia))
        conn.commit()
        print(f"[◦A] Success: Century {century} pulse recorded. Inertia: {inertia}")
    except Exception as e:
        print(f"[Ex ◦] Failed to execute pulse: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    current_t = get_current_state()
    next_t = current_t + 1
    print(f"[◦A] Current Century: {current_t}. Initiating Pulse for Century {next_t}...")
    execute_pulse(next_t)
