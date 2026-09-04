import sqlite3
import json
import os
from typing import Dict, Any, List
from backend.config import settings

class DatabaseManager:
    def __init__(self):
        self.db_path = settings.SQLITE_PATH
        self._init_db()
        self._seed_data()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Cases table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT,
                crime_type TEXT,
                date TEXT,
                location TEXT,
                summary TEXT,
                status TEXT,
                assigned_officer TEXT
            )
        ''')

        # Entities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                entity_id TEXT PRIMARY KEY,
                name TEXT,
                type TEXT,
                details TEXT,
                associated_cases TEXT
            )
        ''')

        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                target TEXT,
                type TEXT,
                confidence REAL,
                case_id TEXT,
                evidence_ref TEXT
            )
        ''')

        # Audit logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                log_id TEXT PRIMARY KEY,
                timestamp TEXT,
                user TEXT,
                action TEXT,
                details TEXT
            )
        ''')

        # Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                insight_id TEXT PRIMARY KEY,
                action TEXT,
                notes TEXT,
                timestamp TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def _seed_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM cases')
        if cursor.fetchone()[0] == 0 and os.path.exists(settings.DATASET_PATH):
            with open(settings.DATASET_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Insert Cases
            for c in data.get('cases', []):
                cursor.execute('''
                    INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (c['case_id'], c['title'], c['crime_type'], c['date'], c['location'], c['summary'], c['status'], c['assigned_officer']))

            # Insert Persons
            for p in data.get('persons', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?)
                ''', (p['person_id'], p['name'], 'Person', json.dumps(p), json.dumps(p.get('associated_cases', []))))

            # Insert Vehicles
            for v in data.get('vehicles', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?)
                ''', (v['vehicle_id'], v['plate_number'], 'Vehicle', json.dumps(v), json.dumps(v.get('associated_cases', []))))

            # Insert Comms
            for cm in data.get('communications', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?)
                ''', (cm['comm_id'], cm['identifier'], 'Communication', json.dumps(cm), json.dumps(cm.get('associated_cases', []))))

            # Insert Locations
            for loc in data.get('locations', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?)
                ''', (loc['location_id'], loc['name'], 'Location', json.dumps(loc), json.dumps(loc.get('associated_cases', []))))

            # Insert Relationships
            for rel in data.get('relationships', []):
                cursor.execute('''
                    INSERT INTO relationships (source, target, type, confidence, case_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (rel['source'], rel['target'], rel['type'], rel['confidence'], rel['case_id']))

            conn.commit()
        conn.close()

    def get_all_cases(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cases')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_entities(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entities')
        rows = cursor.fetchall()
        conn.close()
        result = []
        for r in rows:
            item = dict(r)
            item['details'] = json.loads(item['details']) if item['details'] else {}
            item['associated_cases'] = json.loads(item['associated_cases']) if item['associated_cases'] else []
            result.append(item)
        return result

    def get_all_relationships(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM relationships')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_audit_log(self, user: str, action: str, details: str):
        import datetime
        conn = self.get_connection()
        cursor = conn.cursor()
        log_id = f"LOG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        ts = datetime.datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?)
        ''', (log_id, ts, user, action, details))
        conn.commit()
        conn.close()

    def get_audit_logs(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM audit_logs ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

db_manager = DatabaseManager()
