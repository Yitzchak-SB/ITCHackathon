from flask import Flask
import sqlite3

from data.DataLayer import DataLayer


class SqlDataLayer(DataLayer):
    def __init__(self):
        super.__init__()
        self.connect()

    def __connect(self):
        pass
