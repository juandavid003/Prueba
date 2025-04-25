
import os
import pandas as pd
import shutil
import mysql.connector
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "../input-labs")
PROCESSED_DIR = os.path.join(BASE_DIR, "../processed")
ERROR_DIR = os.path.join(BASE_DIR, "../error")
CONFIG_PATH = os.path.join(BASE_DIR, "../config/db_config.json")

def get_connection():
    with open(CONFIG_PATH, 'r') as f:
        cfg = json.load(f)
    return mysql.connector.connect(
        host=cfg['host'],
        user=cfg['user'],
        password=cfg['password'],
        database=cfg['database']
    )

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        required_cols = {"laboratorio_id", "paciente_id", "tipo_examen", "resultado", "fecha_examen"}
        return required_cols.issubset(df.columns)
    except Exception as e:
        print(f"[ERROR] Falló validación de {file_path}: {e}")
        return False

def process_files():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".csv"):
            path = os.path.join(INPUT_DIR, filename)
            print(f"[INFO] Procesando archivo: {filename}")
            if validate_csv(path):
                insert_into_db(path)
                shutil.move(path, os.path.join(PROCESSED_DIR, filename))
                print(f"[INFO] Archivo {filename} procesado y movido a /processed")
            else:
                shutil.move(path, os.path.join(ERROR_DIR, filename))
                print(f"[WARNING] Archivo {filename} inválido y movido a /error")

def insert_into_db(file_path):
    df = pd.read_csv(file_path)
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT IGNORE INTO resultados_examenes (laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row['laboratorio_id'],
                row['paciente_id'],
                row['tipo_examen'],
                row['resultado'],
                row['fecha_examen']
            ))
        except Exception as e:
            print(f"[ERROR] Insertando fila: {e}")
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_files()
