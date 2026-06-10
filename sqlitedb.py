import sqlite3

def init_db():
    conn = sqlite3.connect("ndf.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ndf_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        image_path TEXT NOT NULL,
        note_de_frais TEXT,
        type_de_charge TEXT,
        compte_comptable INTEGER,
        fournisseur TEXT,
        date TEXT,
        heure TEXT,
        montant_ttc REAL,
        tva REAL,
        taux_tva REAL,
        devise TEXT,
        description TEXT,
        confiance TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_ndf(image_path: str, data: dict):
    conn = sqlite3.connect("ndf.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ndf_data (
            image_path,
            note_de_frais,
            type_de_charge,
            compte_comptable,
            fournisseur,
            date,
            heure,
            montant_ttc,
            tva,
            taux_tva,
            devise,
            description,
            confiance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        image_path,
        data.get("note_de_frais"),
        data.get("type_de_charge"),
        data.get("compte_comptable"),
        data.get("fournisseur"),
        data.get("date"),
        data.get("heure"),
        data.get("montant_ttc"),
        data.get("tva"),
        data.get("taux_tva"),
        data.get("devise"),
        data.get("description"),
        data.get("confiance")
    ))

    conn.commit()
    conn.close()