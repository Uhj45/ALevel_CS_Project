import sqlite3
class BaseDatabase:
    def __init__(self, db_name="sensor.db"):
        self.db_name = db_name
        self.table_name = None
        self.columns = None
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()


class StoreReadings(BaseDatabase):
    pass


class StorePidConstants(BaseDatabase):
    pass

