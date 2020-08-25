from data.DataLayer import DataLayer
import mysql.connector
from decouple import config

class SqlDataLayer(DataLayer):
    def __init__(self):
        super().__init__()
        self.__connect()

    def __connect(self):
        try:
            self.__my_sql = mysql.connector.connect(
                host="127.0.0.1",
                user=config('MYSQL_USER'),
                password=config('PASSWORD'),
                database='roofarm'
            )
        except Exception as e:
            print(e)

    def close(self):
        self.__my_sql.close()

    def add_address(self, lat, long):
        cursor = self.__my_sql.cursor()
        try:
            self.__my_sql.start_transaction()
            sql = 'INSERT INTO addresses (lat, long) VALUES (%s, %s)'
            values = (lat, long,)
            cursor.execute(sql, values)
            self.__my_sql.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()

    def add_result(self, result, address_id):
        cursor = self.__my_sql.cursor()
        try:
            sql = 'INSERT INTO results (res, id_address) VALUES (%s, %s)'
            values = (result, address_id)
            cursor.execute(sql, values)
            return "Inserted successfully " + cursor.rowcount
        finally:
            cursor.close()

    def add_email(self, email, lat, long):
        cursor = self.__my_sql.cursor()
        try:
            user_address_id = None
            user_result_id = None
            sql_address = 'SELECT idaddresses FROM addresses ' \
                          'WHERE lat=%s, long=%s'
            address_values = (lat, long)
            cursor.execute(sql_address, address_values)
            self.__my_sql.commit()
            for (id_address) in cursor:
                user_address_id = id_address
            sql_result = 'SELECT id_address FROM roofarm.results ' \
                         'JOIN roofarm.addresses ' \
                         'WHERE addresses.lat = %s AND addresses.long = %s'
            result_values = (lat, long)
            cursor.execute(sql_result, result_values)
            for (id_result) in cursor:
                user_result_id = id_result
            sql_email = 'INSERT INTO users (email, id_user_address, id_user_result) VALUES (%s, %s, %s)'
            user_values = (email, user_address_id, user_result_id)
            cursor.execute(sql_email, user_values)
            self.__my_sql.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()

    def get_all_data(self):
        cursor = self.__my_sql.cursor()
        user = {}
        try:
            sql = "SELECT * FROM roofarm.addresses " \
                  "INNER JOIN roofarm.results " \
                  "ON addresses.idaddresses = results.id_address " \
                  "INNER JOIN roofarm.users " \
                  "ON addresses.idaddresses = users.id_user_address;"
            cursor.execute()
            for (idaddresses, lat, long, idresults, result, id_address, idusers, email,
                 id_user_address, id_user_result) in cursor:
                user[idusers] = {
                    "email": email,
                    "latitude": lat,
                    "longitude": long,
                    "result": result
                }
                return user
        finally:
            cursor.close()
            