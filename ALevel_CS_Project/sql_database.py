import sqlite3
class BaseDatabase:
    """
    Class provides the basic common methods to use the database
    The user is not expected to use this base class instead
    create a new subclass and inherit the base attributes and methods
    The subclass should be customised by changing the table name and the columns
    """
    def __init__(self, db_name="test.db"):
        """
        This initialises the database connection
        :param db_name: Needs to be specified, or it will be set to its default
        """
        self.db_name = db_name
        self.table_name = None
        self.columns = None
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()

    def create_table(self):
        self.table_name = "people"
        self.columns = """
        first_name text,
        last_name text,
        email text,
        age int
        """
        table = f"""CREATE TABLE {self.table_name}(
        {self.columns}
        )"""
        self.cursor.execute(table)
        self.db_connection.commit()

    def add_item(self):
        many_customers = [
             ('Wes', 'Brown', 'wes@brown.com', 23),
             ('Steph', 'Kuewa', 'steph@kuewa.com', 56),
             ('Dan', 'Pas', 'dan@pas.com', 47),
         ]

        self.cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?,?,?,?)", many_customers)
        self.db_connection.commit()

    def remove_item(self):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = 4")
        self.db_connection.commit()

    def update_item(self):
        self.cursor.execute(f"""UPDATE {self.table_name} SET {self.columns} = 'Bob'
                WHERE {self.columns} = 'Elder'
                """)
        self.db_connection.commit()

    def get_item(self):
        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE rowid = 3""")


class StoreReadings(BaseDatabase):
    def __init__(self, db_name="Senors.db", table_name="Senors Readings"):
        super().__init__(db_name)
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()
        self.db_name = db_name
        self.table_name = table_name
        self.columns = """
        Height int,
        Target Height int,
        LED1 text,
        LED2 text,
        Fan Speed int,
        Time int
        """
    def create_table(self):
        table = f"""CREATE TABLE {self.table_name}(
        {self.columns}
        )"""
        self.cursor.execute(table)
        self.db_connection.commit()
    def add_item(self):
        sensor_readings = [

        ]
        self.cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?,?,?,?)", sensor_readings)
        self.db_connection.commit()

    def remove_item(self):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = 4")
        self.db_connection.commit()

    def update_item(self):
        self.cursor.execute(f"""UPDATE {self.table_name} SET {self.columns} = 'Bob'
                WHERE {self.columns} = 'Elder'
                """)
        self.db_connection.commit()

    def get_item(self):
        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE rowid = 3""")


class StorePidConstants(BaseDatabase):
    def __init__(self, db_name, table_name, columns):
        super().__init__(db_name)
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()
        self.db_name = "PID Constants Database"
        self.table_name = "PID Constants"
        self.columns = """
        Kp int,
        Ki int,
        Kd int
        """

    def create_table(self):
        table = f"""CREATE TABLE {self.table_name}(
        {self.columns}
        )"""
        self.cursor.execute(table)
        self.db_connection.commit()

    def add_item(self):
        values = [
            '23',
            '45',
            '67',
        ]
        self.cursor.execute(f"""INSERT INTO """)
        self.db_connection.commit()

test = BaseDatabase()
test.create_table()
test1 = StoreReadings()
test1.create_table()
