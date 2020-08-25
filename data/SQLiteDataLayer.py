from flask import Flask
import sqlite3
from decouple import config
from data.DataLayer import DataLayer


class SqlDataLayer(DataLayer):
    def __init__(self):
        super.__init__(self)
        self.connect()

    def __connect(self):
        try:
            self.__sqliteDb = sqlite3.connect(
                host="127.0.0.1",
                user=config('USER'),
                password=config('PASSWORD'),
                database='roofarm'
            )
        except Exception as e:
            print(e)

    def close(self):
        self.__sqliteDb.close()

    def add_user(self, lat, long):
        cursor = self.__sqliteDb.cursor()
        try:
            self.__sqliteDb.start_transaction()
            sql = 'INSERT INTO addresses (lat, long) VALUES (%s, %s)'
            values = (lat, long,)
            cursor.execute(sql, values)
            self.__sqliteDb.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()

    def add_email_to_user(self, email, lat, long):
        cursor = self.__sqliteDb.cursor()
        try:
            user_id = cursor.lastrowid
            self.__sqliteDb.start_transaction()
            sql_address = 'SELECT idaddresses FROM addresses ' \
                          'WHERE lat=%s, long=%s'
            values = (lat, long)
            cursor.execute(sql_address, values)
            sql_email = 'INSERT INTO users (email) VALUES (%s)'
            value = (email,)

            self.__sqliteDb.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()
