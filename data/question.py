import psycopg2

## Bu değeri localinde çalışırken kendi passwordün yap. Ama kodu pushlarken 'postgres' olarak bırak.
password = '1907'

def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=password
    )

# 1- Null emailleri 'unknown@example.com' ile değiştir
def clean_null_emails():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE data5.customers 
SET email = 'unknown@example.com' 
WHERE email IS NULL;""")
            conn.commit()

# 2- Hatalı emailleri bul
def find_invalid_emails():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT * 
FROM data5.customers 
WHERE email NOT LIKE '%@%';
""")
            return cur.fetchall()

# 3- İsimlerin ilk 3 harfi
def get_first_3_letters_of_names():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT full_name, LEFT(full_name, 3) AS short_name
FROM data5.customers;""")
            return cur.fetchall()

# 4- Email domainlerini bul
def get_email_domains():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT full_name,
       SUBSTRING(email FROM POSITION('@' IN email) + 1) AS domain
FROM data5.customers;""")
            return cur.fetchall()

# 5- İsim ve email birleştir
def concat_name_and_email():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT CONCAT(full_name, ' - ', email) AS full_info 
FROM data5.customers;""")
            return cur.fetchall()

# 6- Sipariş tutarlarını tam sayıya çevir
def cast_total_amount_to_integer():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT order_id, CAST(total_amount AS INTEGER) AS total_amount_int
FROM data5.orders;
""")
            return cur.fetchall()

# 7- Email '@' pozisyonu
def find_at_position_in_email():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT full_name, POSITION('@' IN email) AS at_position
FROM data5.customers;""")
            return cur.fetchall()

# 8- NULL kategoriye 'Unknown' yaz
def fill_null_product_category():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT product_name, COALESCE(category, 'Unknown') AS product_category
FROM data5.products;""")
            return cur.fetchall()

# 9- Müşteri harcama sıralaması (RANK)
def rank_customers_by_spending():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT customer_id, total_amount, 
       RANK() OVER (ORDER BY SUM(total_amount) DESC) AS rank_by_spend 
FROM data5.orders
GROUP BY customer_id, total_amount;""")
            return cur.fetchall()

# 10- Müşteri siparişlerinde running total
def running_total_per_customer():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT order_id, customer_id, total_amount,
       SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_id) AS running_total
FROM data5.orders
LIMIT 3;
""")
            return cur.fetchall()

# 11- Elektronik ve Beyaz Eşya ürünleri (UNION)
def get_electronics_and_appliances():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT product_name, category FROM data5.products WHERE category = 'Electronics'
UNION
SELECT product_name, category FROM data5.products WHERE category = 'Appliances';""")
            return cur.fetchall()

# 12- Tüm siparişler ve eksik siparişler (UNION ALL)
def get_orders_with_missing_customers():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT c.customer_id, o.total_amount
FROM data5.customers c
LEFT JOIN data5.orders o ON c.customer_id = o.customer_id;""")
            return cur.fetchall()