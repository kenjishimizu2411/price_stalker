import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
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

# --- NOVAS FUNÇÕES DE USUÁRIO ---

def create_user(name, email, password_hash, phone):
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash, phone) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, email, password_hash, phone)
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
        # Busca o usuário pelo email
        cur.execute("SELECT id, name, email, password_hash, phone FROM users WHERE email = %s", (email,))
        return cur.fetchone() # Retorna a tupla ou None
    except Exception:
        return None
    finally:
        conn.close()

# --- FUNÇÕES DE PRODUTO ATUALIZADAS ---

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
    """
    Busca produtos onde:
    (Agora) > (Ultima Vez + Intervalo)
    OU
    Nunca foi checado (last_checked_at IS NULL)
    """
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        query = """
        SELECT p.id, p.name, p.url, p.target_price, u.phone, u.name
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
        # Primeiro remove o histórico (porque depende do produto)
        cur.execute("DELETE FROM price_history WHERE product_id = %s", (product_id,))
        # Depois remove o produto
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro delete: {e}")
        return False
    finally:
        conn.close()