from database.DB_connect import DBConnect
from model.categorie import Categoria
from model.prodotti import Prodotto
from model.connessioni import Connessione


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def get_categorie():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select c.id , c.category_name 
                    from category c"""
        cursor.execute(query)
        for row in cursor:
            results.append(Categoria(row["id"], row["category_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_prodotti(categoria):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select p.id , p.product_name  
                    from product p, category c 
                    where p.category_id = c.id and c.id = %s"""
        cursor.execute(query, (categoria, ))
        for row in cursor:
            results.append(Prodotto(row["id"], row["product_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_connessioni(categoria, data_inizio, data_fine):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select p.id , p.product_name, sum(oi.quantity) as num_vendite
                    from product p, category c, order_item oi, `order` o  
                    where p.category_id = c.id and c.id = %s and oi.product_id = p.id
                    and o.id = oi.order_id and o.order_date between %s and %s
                    group by p.id"""
        cursor.execute(query, (categoria, data_inizio, data_fine ))
        for row in cursor:
            results.append(Connessione(row["id"], row["product_name"], row["num_vendite"]))

        cursor.close()
        conn.close()
        return results

