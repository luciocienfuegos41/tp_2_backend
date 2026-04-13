import mysql.connector
from config import DB_CONFIG


def crear_partido(equipo_local, equipo_visitante, estadio, ciudad, fecha, fase):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
        INSERT INTO partidos (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase))
    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return nuevo_id

def get_partidos():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
        SELECT * FROM usuarios;
    """

