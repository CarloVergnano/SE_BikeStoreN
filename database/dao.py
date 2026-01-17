from database.DB_connect import DBConnect
from model.categorie import Categoria
from model.prodotti import Prodotto
from model.vendite import Vendita


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
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                    select *
                    from bike_store_full.category
                    order by id
                    """
        try:
            cursor.execute(query)
            for row in cursor:
                categoria = Categoria(
                    id=row["id"],
                    category_name=row["category_name"],
                )
                result.append(categoria)

        except Exception as e:
            print(f"Errore durante la query get_categoria: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_prodotti(categoria):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                        select distinct id, product_name
                        from bike_store_full.product
                        where category_id = %s
                        order by id
                        """
        try:
            cursor.execute(query, (categoria,))
            for row in cursor:
                prodotto = Prodotto(
                    id=row["id"],
                    product_name=row["product_name"],
                )
                result.append(prodotto)

        except Exception as e:
            print(f"Errore durante la query get_prodotti: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_vendite(start, end, categoria):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                           select oi1.product_id, count(*) as num_vendite
                           from bike_store_full.order_item as oi1
                           where oi1.order_id in (SELECT o1.id as id_ordini
                                                  FROM bike_store_full.`order` o1
                                                  where o1.order_date between %s and %s 
                                                  order by id_ordini)
                           and oi1.product_id in (select distinct id
                                                  from bike_store_full.product
                                                  where category_id = %s
                                                  order by id)
                           group by oi1.product_id
                           order by oi1.product_id
                           """
        try:
            cursor.execute(query, (start, end, categoria))
            for row in cursor:
                vendita = Vendita(
                    product_id=row["product_id"],
                    num_vendite=row["num_vendite"],
                )
                result.append(vendita)

        except Exception as e:
            print(f"Errore durante la query get_vendite: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result