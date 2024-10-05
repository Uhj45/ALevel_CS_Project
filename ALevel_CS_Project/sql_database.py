import sqlite3
import time

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
        self.table_name = "people"
        self.columns = """
        first_name text,
        last_name text,
        email text,
        age int,
        car text,
        clothes text,
        accessory text,
        pet text
        job text
        company text
        kids int
        """
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()

    def create_table(self):
        table = f"""CREATE TABLE {self.table_name}(
        {self.columns}
        )"""
        self.cursor.execute(table)
        self.db_connection.commit()

    def add_item(self, name, lastname, email, age, car, clothes, accessory, pet, job, kids):           # Had to add parameters here to match the parameters used in the subclass
        many_customers = [
             (f'{name}', f'{lastname}', f'{email}', f'{age}', f'{car}'),
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
    def __init__(self, db_name="SensorData.db", table_name="SensorResults"):
        super().__init__(db_name)
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()
        self.db_name = db_name
        self.table_name = table_name
        self.columns = """
        RunID int,
        Time int,
        Height int,
        Target Height int,
        Threshold int,
        Upper_Threshold int,
        Lower_Threshold int,
        Float text,
        Kp DEFAULT 0,
        Ki DEFAULT 0,
        Kd DEFAULT 0
        """
    # def create_table(self):
    #     table = f"""CREATE TABLE {self.table_name}(
    #     {self.columns}
    #     )"""
    #     self.cursor.execute(table)
    #     self.db_connection.commit()
    def add_item(self, runid, height, target_height, threshold, upper_threshold, lower_threshold, floats, kp, ki, kd):
        epoch_time = int(time.time())
        sensor_readings = [(f'{runid}', f'{epoch_time}', f'{height}', f'{target_height}', f'{threshold}', f'{upper_threshold}', f'{lower_threshold}', f'{floats}' f'{kp}', f'{ki}', f'{kd}')]
        self.cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?,?,?,?,?,?,?,?,?,?,?)", sensor_readings)
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        items = self.cursor.fetchall()
        for item in items:
            print(item)
        self.db_connection.commit()

    def remove_item(self):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = 3")
        self.db_connection.commit()

    def update_item(self):
        self.cursor.execute(f"""UPDATE {self.table_name} SET LED1 = 'Off'
                WHERE rowid = 1
                """)
        self.db_connection.commit()

    def get_item(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE Height > 12")
        query_result1 = self.cursor.fetchall()
        for item in query_result1:
            print(item)


class StorePidConstants(BaseDatabase):
    def __init__(self, db_name="Sensors.db", table_name="PIDConstants"):
        super().__init__(db_name)
        self.db_filename = f"./sqlite/{self.db_name}"
        self.db_connection = sqlite3.connect(self.db_filename)
        self.cursor = self.db_connection.cursor()
        self.db_name = db_name
        self.table_name = table_name
        self.columns = """
        Kp int,
        Ki int,
        Kd int
        """

    # def create_table(self):
    #     table = f"""CREATE TABLE {self.table_name}(
    #     {self.columns}
    #     )"""
    #     self.cursor.execute(table)
    #     self.db_connection.commit()

    def add_item(self):
        values = [
            ('23', '45', '65'),
            ('12', '90', '37'),
            ('23', '9', '15'),
        ]
        self.cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?,?,?)", values)
        self.db_connection.commit()

    def get_item(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE Kp = '56' ")
        query_result2 = self.cursor.fetchall()
        for item in query_result2:
            print(item)

    def remove_item(self):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = 1")
        self.db_connection.commit()

    def update_item(self):
        self.cursor.execute(f"UPDATE {self.table_name} SET Kp = '56' WHERE rowid = 2 ")
        self.db_connection.commit()


# test = StoreReadings()
# test.create_table()
# test.add_item(1, 20, 2, 22, 18, 6, 7, 8, 9)
# test.remove_item()
# test.get_item()
# test.update_item()

# test1 = StorePidConstants()
# test1.create_table()
# test1.add_item()
# test1.get_item()
# test1.remove_item()
# test1.update_item()
