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

def get_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
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

    count_cursor = conn.cursor()
    count_cursor.execute("SELECT COUNT(*) FROM (" + sql + ") AS total", params)
    total = count_cursor.fetchone()[0]
    count_cursor.close()

    sql += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(sql, params)
    partidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return partidos, total

def get_partido_by_id(partido_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    sql = "SELECT * FROM partidos WHERE id = %s"
    cursor.execute(sql, (partido_id,))
    partido = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return partido


def actualizar_resultado(partido_id, goles_local, goles_visitante):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    cursor.execute("""
        UPDATE partidos
        SET goles_local = %s,
            goles_visitante = %s
        WHERE id = %s
    """, 
    (goles_local, goles_visitante, partido_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True


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

def reemplazar_partido(partido_id, equipo_local, equipo_visitante, estadio, ciudad, fecha, fase):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    cursor.execute("""
        UPDATE partidos
        SET equipo_local = %s, equipo_visitante = %s, estadio = %s, ciudad = %s, fecha = %s, fase = %s
        WHERE id = %s
    """, (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase, partido_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True


def actualizar_partido_parcial(partido_id, campos_a_actualizar):

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    set_query = ", ".join([f"{campo} = %s" for campo in campos_a_actualizar.keys()])
    
    valores = list(campos_a_actualizar.values())
    valores.append(partido_id) 

    sql = f"UPDATE partidos SET {set_query} WHERE id = %s"

    try:
        cursor.execute(sql, valores)
        conn.commit()
        
        filas_afectadas = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        return filas_afectadas > 0

    except Exception as e:
        print(f"Error en PATCH: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False
    
def guardar_prediccion(partido_id, id_usuario, local, visitante):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error:
        raise Exception
    cursor = conn.cursor()


    cursor.execute("SELECT id FROM partidos WHERE id = %s", (partido_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return 1
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id_usuario,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return 2

    try:
        cursor.execute("INSERT INTO prediccion (id_usuario, id_partido, goles_local, goles_visitante) VALUES (%s,%s,%s,%s)", (id_usuario, partido_id, local, visitante))
        conn.commit()
    except mysql.connector.IntegrityError:
        cursor.close()
        conn.close()
        raise NotImplementedError
    
    cursor.close()
    conn.close()
    return True
    

    

