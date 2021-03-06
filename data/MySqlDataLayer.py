import mysql.connector
from flask import Flask, json

from hackaton_ds import find_roof_json


class MySqlDataLayer:

    @staticmethod
    def _connect():
        try:
            connection = mysql.connector.connect(
                host="us-cdbr-east-02.cleardb.com",
                user=" ba735323da93cc",
                password="e0779887",
                database="heroku_67f25d3137a219d"
            )
            return connection
        except Exception as e:
            print("connection error: {}".format(e))

    @staticmethod
    def get_all():
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            sql = "SELECT * FROM addresses"
            cursor.execute(sql,)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_address(lat, long):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO roofarm.addresses (latitude, longitude) VALUES (%s, %s)"
            values = (lat, long)
            cursor.execute(sql, values)
            print("Success")
            connection.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + str(count))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_result(latitude, longitude):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            res = None
            adr_id = None
            sql_address = "SELECT idaddresses " \
                          "FROM roofarm.addresses " \
                          "WHERE latitude = %s" \
                          "AND longitude = %s"
            values_address = (latitude, longitude)
            cursor.execute(sql_address, values_address)
            for (address_id) in cursor:
                adr_id = address_id
                print(adr_id)
            sql = "SELECT result FROM roofarm.results " \
                  "JOIN roofarm.addresses " \
                  "ON results.id_address = addresses.idaddresses " \
                  "WHERE results.id_address = %s"
            value = adr_id
            cursor.execute(sql, value)
            print("Success")
            for (result) in cursor:
                print(result)
                res = result
                print(res)
            return res
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_result(result, address_id):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO results (res, id_address) VALUES (%s, %s)"
            values = (result, address_id)
            cursor.execute(sql, values)
            return "Inserted successfully " + cursor.rowcount
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_email(email, latitude, longitude):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            user_address_id = None
            user_result_id = None
            sql_address = 'SELECT idaddresses FROM roofarm.addresses ' \
                          'WHERE latitude=%s AND longitude=%s'
            address_values = (latitude, longitude)
            cursor.execute(sql_address, address_values)
            for (id_address) in cursor:
                user_address_id = id_address
            sql_result = 'SELECT idresults FROM roofarm.results ' \
                         'WHERE id_address=%s'
            result_value = user_address_id
            cursor.execute(sql_result, result_value)
            for (id_result) in cursor:
                user_result_id = id_result
            sql_email = 'INSERT INTO users (email, id_user_address, id_user_result) VALUES (%s, %s, %s)'
            user_values = (email, user_address_id[0], user_result_id[0])
            cursor.execute(sql_email, user_values)
            connection.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + str(count))
        except Exception as e:
            print(e)
            return e
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_data():
        user = {}
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            sql = "SELECT * FROM addresses " \
                  "INNER JOIN results " \
                  "ON addresses.idaddresses = results.id_address " \
                  "INNER JOIN roofarm.users " \
                  "ON addresses.idaddresses = users.id_user_address;"
            cursor.execute(sql)
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
            connection.close()

    @staticmethod
    def json_to_db():
        results = []
        connection = MySqlDataLayer._connect()
        cursor = connection.cursor()
        address_string = None
        latitude = None
        longitude = None
        location_type = None
        place_id = None
        sqr_meters = None
        address_id = None
        try:
            with open('.\\data\\roofs2.json', 'r') as read_file:
                roofs = json.load(read_file)
                for i in range(0, 5535):
                    result = {}
                    for (key, value) in roofs.items():
                        result[key] = value[str(i)]
                    results.append(result)
                for i in results:
                    address_string = i['AddressString']
                    latitude = i['AddLat']
                    longitude = i['AddLng']
                    sqr_meters = i['sqrd_meters']
                    address_id = i['address_id']
                    try:
                        cursor = connection.cursor()
                        sql = "INSERT INTO france_adr (id_address, latitude, longitude, address_str, " \
                              "square_mtr) VALUES (%s, %s, %s, %s, %s)"
                        values = (address_id, latitude, longitude, address_string, sqr_meters)
                        cursor.execute(sql, values)
                        connection.commit()
                        count = cursor.rowcount
                        return ("Inserted successfully " + str(count))
                    except Exception as e:
                        print(e)
                    finally:
                        cursor.close()
                        connection.close()
                return results
        except FileNotFoundError as e:
            print(e)

    @staticmethod
    def get_square(latitude, longitude):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            result = None
            sql = "SELECT sqrd_meters FROM france_adr WHERE add_lat = %s AND add_lng = %s"
            values = (latitude, longitude)
            cursor.execute(sql, values)
            for res in cursor:
                result = res
            return result
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_data_from_input(latitude, longitude, address):
        try:
            connection = MySqlDataLayer._connect()
            cursor = connection.cursor()
            res_exists = None
            res_square = None

            sql = "SELECT EXISTS(SELECT * FROM france_adr " \
                  "WHERE latitude = %s AND longitude = %s);"
            values = (latitude, longitude)
            cursor.execute(sql, values)
            for i in cursor:
                res_exists = i
            print(res_exists[0])
            if res_exists[0] == 1:
                sql = "SELECT square_mtr FROM france_adr WHERE latitude = %s AND longitude = %s"
                values = (latitude, longitude)
                cursor.execute(sql, values)
                for res in cursor:
                    res_square = res
                print(res_square[0])
                return res_square[0]
            elif res_exists[0] == 0:
                calculation = find_roof_json(latitude, longitude, address)
                print(calculation)
                sql_ins = "INSERT INTO france_adr (id_address, latitude, longitude, address_str, " \
                              "square_mtr) VALUES (%s, %s, %s, %s, %s)"
                values_ins = (calculation[0], str(calculation[1]), str(calculation[2]),
                              calculation[3], str(calculation[4]))
                cursor.execute(sql_ins, values_ins)
                print("Inserted " + str(cursor.rowcount))
                connection.commit()
                return calculation[4]
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()
            connection.close()
