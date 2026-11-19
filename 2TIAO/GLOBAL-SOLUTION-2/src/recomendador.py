import csv
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "pontos.csv"
MATERIAIS = ("Papel", "Plástico", "Vidro", "Metal", "Eletrônicos", "Óleo de cozinha")

@contextmanager
def catalogo():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    try:
        db.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE ponto (
                id INTEGER PRIMARY KEY, nome TEXT NOT NULL,
                bairro TEXT NOT NULL, sabado INTEGER CHECK (sabado IN (0, 1))
            );
            CREATE TABLE aceite (
                ponto_id INTEGER REFERENCES ponto(id), material TEXT NOT NULL,
                PRIMARY KEY (ponto_id, material)
            );
        """)
        with BASE.open(encoding="utf-8", newline="") as arquivo:
            for linha in csv.DictReader(arquivo):
                ponto_id = int(linha["id"])
                db.execute("INSERT INTO ponto VALUES (?, ?, ?, ?)", (
                    ponto_id, linha["nome"].strip(), linha["bairro"].strip(),
                    int(linha["sabado"]),
                ))
                db.executemany("INSERT INTO aceite VALUES (?, ?)", [
                    (ponto_id, material.strip())
                    for material in linha["materiais"].split("|")
                ])
        yield db
    finally:
        db.close()

def recomendar(db, bairro, material, somente_sabado=False):
    return db.execute("""
        SELECT p.*, (p.bairro = ?) AS no_bairro
        FROM ponto AS p JOIN aceite AS a ON a.ponto_id = p.id
        WHERE a.material = ? AND (? = 0 OR p.sabado = 1)
        ORDER BY no_bairro DESC, p.nome COLLATE NOCASE, p.id
    """, (bairro, material, int(somente_sabado))).fetchall()

def cobertura(db):
    return db.execute("""
        SELECT material, COUNT(*) AS total
        FROM aceite GROUP BY material
        ORDER BY total DESC, material
    """).fetchall()
