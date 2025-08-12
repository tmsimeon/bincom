#!/usr/bin/env python3
"""
Full script:
- create DB if missing
- run migrations (create baby_names table)
- read baby2008.html and extract rank/male/female via regex
- insert names into DB (ON CONFLICT DO NOTHING)
- provide selection sorts and binary-search (male & female)
"""

import re
import sys
import psycopg2
from psycopg2 import sql

# -------- CONFIG --------
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "bincom"   # <-- change if different
DB_NAME = "bincom_db"
TABLE_NAME = "baby_names"
HTML_FILE = "baby2008.html"

# -------- DB helpers --------
def connect_default():
    """Connect to default 'postgres' DB for admin tasks."""
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname="postgres")

def connect_db():
    """Connect to the application DB (DB_NAME)."""
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)

def database_exists(cur, name):
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (name,))
    return cur.fetchone() is not None

def create_database():
    """Create DB if it doesn't exist."""
    try:
        conn = connect_default()
        conn.autocommit = True
        cur = conn.cursor()
        if database_exists(cur, DB_NAME):
            print(f"[DB] Database '{DB_NAME}' already exists.")
        else:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"[DB] Database '{DB_NAME}' created.")
        cur.close()
        conn.close()
    except Exception as e:
        print("[ERROR] create_database:", e)
        sys.exit(1)

def run_migrations():
    """Create baby_names table if not exists (and ensure rank is PK)."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                rank INTEGER PRIMARY KEY,
                male VARCHAR(200),
                female VARCHAR(200),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            );
        """).format(sql.Identifier(TABLE_NAME)))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Table '{TABLE_NAME}' is ready.")
    except Exception as e:
        print("[ERROR] run_migrations:", e)
        sys.exit(1)

# -------- Parsing HTML --------
def parse_baby_html(path):
    """Read HTML file and extract rank, male, female into a dict {rank: (male,female)}."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"[ERROR] HTML file '{path}' not found. Put it in the same folder and try again.")
        sys.exit(1)

    # Robust regex: allow whitespace inside tags and names with letters, hyphens, apostrophes
    pattern = r"<tr[^>]*>\s*<td>\s*(\d+)\s*</td>\s*<td>\s*([A-Za-z'\-]+)\s*</td>\s*<td>\s*([A-Za-z'\-]+)\s*</td>"
    matches = re.findall(pattern, html)
    baby_dict = {int(rank): (male, female) for rank, male, female in matches}
    print(f"[PARSE] Extracted {len(baby_dict)} rows from '{path}'.")
    return baby_dict

# -------- DB Insert --------
def save_baby_names_to_db(baby_dict):
    """Insert baby names into DB; skip duplicates by rank."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        insert_q = sql.SQL("INSERT INTO {} (rank, male, female) VALUES (%s, %s, %s) ON CONFLICT (rank) DO NOTHING;").format(sql.Identifier(TABLE_NAME))
        for rank, (male, female) in baby_dict.items():
            cur.execute(insert_q, (rank, male, female))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Inserted/updated {len(baby_dict)} records (duplicates by rank were ignored).")
    except Exception as e:
        print("[ERROR] save_baby_names_to_db:", e)
        sys.exit(1)

def fetch_all_baby_names():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT rank, male, female FROM {} ORDER BY rank;").format(sql.Identifier(TABLE_NAME)))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("[ERROR] fetch_all_baby_names:", e)
        return []

# -------- Sorting & Searching (pure Python) --------
def selection_sort_by_rank(data):
    items = list(data.items())  # [(rank, (male,female)), ...]
    n = len(items)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if items[j][0] < items[min_idx][0]:
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items  # list of (rank, (male,female))

def selection_sort_by_name(data, gender="male"):
    # gender: "male" or "female"
    items = [(rank, male, female) for rank, (male, female) in data.items()]
    n = len(items)
    idx = 1 if gender == "male" else 2
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if items[j][idx].lower() < items[min_idx][idx].lower():
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items  # list of (rank, male, female)

def binary_search_on_sorted_by_key(sorted_list, name, gender="male"):
    """Binary search on a list sorted by the chosen gender name.
    sorted_list is list of (rank,male,female). gender chooses which field to compare."""
    low = 0
    high = len(sorted_list) - 1
    key_idx = 1 if gender == "male" else 2
    name_lower = name.lower()
    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_list[mid][key_idx].lower()
        if name_lower == mid_name:
            return sorted_list[mid]  # (rank, male, female)
        elif name_lower < mid_name:
            high = mid - 1
        else:
            low = mid + 1
    return None

def find_name(data, name):
    """Try binary search on male-sorted list then female-sorted list for efficiency."""
    sorted_by_male = selection_sort_by_name(data, gender="male")
    res = binary_search_on_sorted_by_key(sorted_by_male, name, gender="male")
    if res:
        return res
    sorted_by_female = selection_sort_by_name(data, gender="female")
    res = binary_search_on_sorted_by_key(sorted_by_female, name, gender="female")
    return res

# -------- Main execution --------
if __name__ == "__main__":
    # 1. Create DB (if needed) and run migrations
    create_database()
    run_migrations()

    # 2. Parse HTML file into dictionary
    baby_dict = parse_baby_html(HTML_FILE)

    if not baby_dict:
        print("[WARN] No baby names found — exiting.")
        sys.exit(0)

    # 3. Insert into DB (skip duplicates by rank)
    save_baby_names_to_db(baby_dict)

    # 4. Show first 10 rows read from DB
    rows = fetch_all_baby_names()
    print("\n[DB] Sample rows (first 10):")
    for r in rows[:10]:
        print(r)

    # 5. Demonstrate sorting & searching on the in-memory dict
    sorted_by_rank = selection_sort_by_rank(baby_dict)
    print("\n[PY] Sorted by rank (first 10):")
    for rank, names in sorted_by_rank[:10]:
        print(rank, names)

    sorted_by_male = selection_sort_by_name(baby_dict, gender="male")
    print("\n[PY] Sorted by male name (first 10):")
    for rank, male, female in sorted_by_male[:10]:
        print(rank, male, female)

    # 6. Example search
    query_name = "Jacob"
    found = find_name(baby_dict, query_name)
    if found:
        print(f"\n[SEARCH] Found '{query_name}': Rank {found[0]}, Male={found[1]}, Female={found[2]}")
    else:
        print(f"\n[SEARCH] '{query_name}' not found in parsed data.")
