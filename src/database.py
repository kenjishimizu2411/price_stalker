import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            return psycopg2.connect(database_url)
        
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
    except Exception as e:
        print(f"Erro conexão: {e}")
        return None


def create_user(name, email, password_hash, phone, api_key):
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash, phone, whatsapp_api_key) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (name, email, password_hash, phone, api_key)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print(f"Erro ao criar user: {e}")
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password_hash, phone FROM users WHERE email = %s", (email,))
        return cur.fetchone()
    except Exception:
        return None
    finally:
        conn.close()

def add_product(user_id, name, url, target_price, interval):
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO products (user_id, name, url, target_price, check_interval_hours, last_checked_at) 
               VALUES (%s, %s, %s, %s, %s, NULL)""",
            (user_id, name, url, target_price, interval)
        )
        conn.commit()
    finally:
        conn.close()

def get_products_by_user(user_id):
    """Retorna apenas os produtos daquele usuário específico"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, url, target_price, check_interval_hours FROM products WHERE user_id = %s", (user_id,))
        return cur.fetchall()
    finally:
        conn.close()

def get_due_products():
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        query = """
        SELECT p.id, p.name, p.url, p.target_price, u.phone, u.name, u.whatsapp_api_key
        FROM products p
        JOIN users u ON p.user_id = u.id
        WHERE p.last_checked_at IS NULL 
           OR p.last_checked_at < NOW() - (p.check_interval_hours || ' hours')::INTERVAL
        """
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()

def update_last_checked(product_id):
    """Carimba o cartão de ponto do produto: 'Checado agora!'"""
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE products SET last_checked_at = NOW() WHERE id = %s", (product_id,))
        conn.commit()
    finally:
        conn.close()

def update_product_full(product_id, new_name, new_url, new_target):
    """Atualiza todos os dados do produto"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE products 
               SET name = %s, url = %s, target_price = %s 
               WHERE id = %s""",
            (new_name, new_url, new_target, product_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro update full: {e}")
        return False
    finally:
        conn.close()

def delete_product(product_id):
    """Remove um produto e seu histórico"""
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM price_history WHERE product_id = %s", (product_id,))
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro delete: {e}")
        return False
    finally:
        conn.close()

def get_user_info(user_id):
    """Busca todos os dados do perfil do usuário"""
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, email, phone, whatsapp_api_key FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar user: {e}")
        return None
    finally:
        conn.close()

def update_user_profile(user_id, name, email, phone, api_key):
    """Atualiza os dados cadastrais"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE users 
               SET name = %s, email = %s, phone = %s, whatsapp_api_key = %s 
               WHERE id = %s""",
            (name, email, phone, api_key, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return False
    finally:
        conn.close()