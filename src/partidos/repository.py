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

def get_partidos(equipo=None, fecha=None, fase=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM partidos WHERE 1=1"
    params = []

    if equipo:
        sql += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.extend([equipo, equipo])
    if fecha:
        sql += " AND DATE(fecha) = %s"
        params.append(fecha)
    if fase:
        sql += " AND fase = %s"
        params.append(fase)

    cursor.execute(sql, params)
    partidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return partidos


def eliminar_partido(partido_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    cursor.execute("DELETE FROM partidos WHERE id = %s", (partido_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return True
