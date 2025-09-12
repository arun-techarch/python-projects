from app.services.db import get_cursor
from app.models.customer import Customer

def get_all_customers():
    with get_cursor() as cur:
        cur.execute("SELECT id, name, email, phone, company, city, country FROM customer")
        rows = cur.fetchall()
        print(len(rows))
        return [dict(zip(["id", "name", "email", "phone", "company", "city", "country"], row)) for row in rows]