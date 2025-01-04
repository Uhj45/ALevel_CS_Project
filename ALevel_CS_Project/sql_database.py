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
        pet text,
        job text,
        company text,
        kids int,
        salary int,
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

    def add_item(self, name, lastname, email, age, car, clothes, accessory, pet, job, kids, salary, boss_name, work_location, computer):           # Had to add parameters here to match the parameters used in the subclass
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
    """
    Inherits attributes and functions from base class
    """
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
        Fan_Speed int,
        Float text,
        Kp float,
        P_Term float,
        Ki float,
        I_term float,
        Kd float,
        D_term
        """
    def create_table(self):
        """
        Creates database and tables in the correct directory and with names specified
        :return:
        """
        table = f"""CREATE TABLE {self.table_name}(
        {self.columns}
        )"""
        self.cursor.execute(table)
        self.db_connection.commit()

    def add_item(self, runid, height, target_height, threshold, upper_threshold, lower_threshold,fan_speed, floats, kp, p_term, ki,i_term, kd, d_term):
        """
        Adds values to the database under the columns specified
        :param runid:
        :param height:
        :param target_height:
        :param threshold:
        :param upper_threshold:
        :param lower_threshold:
        :param fan_speed:
        :param floats:
        :param kp:
        :param p_term:
        :param ki:
        :param i_term:
        :param kd:
        :param d_term:
        :return:
        """
        epoch_time = int(time.time())
        sensor_readings = [(f'{runid}',f'{epoch_time}',f'{height}',f'{target_height}',f'{threshold}',f'{upper_threshold}',f'{lower_threshold}',f'{fan_speed}',f'{floats}',f'{kp}',f'{p_term}',f'{ki}',f'{i_term}',f'{kd}',f'{d_term}')]
        # print(sensor_readings)
        self.cursor.executemany(f"INSERT INTO {self.table_name} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", sensor_readings)
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        self.db_connection.commit()

    def remove_item(self):
        """
        Removes item from the database
        :return:
        """
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE rowid = 3")
        self.db_connection.commit()

    def update_item(self):
        """
        Updates a value in the database
        :return:
        """
        self.cursor.execute(f"""UPDATE {self.table_name} SET LED1 = 'Off'
                WHERE rowid = 1
                """)
        self.db_connection.commit()

    def get_item(self):
        """
        This will retrieve all the data with the most recent ID from the database
        :return:
        """
        # Query's the table to get all values from the Height column with the most recent runid value ready to be fetched
        self.cursor.execute(f"SELECT Height,Time, Target Height, Upper_Threshold, Lower_Threshold, Fan_Speed, Kp, Ki, Kd, P_Term, I_Term, D_Term FROM {self.table_name} WHERE runid = (SELECT MAX(runid) FROM {self.table_name})")
        # returns all values that were specified in the query and prints them onto a blank webpage
        return self.cursor.fetchall()

    def get_recent_record(self):
        get_record = self.cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY runid DESC LIMIT 1")
        for item in get_record:
            print(item)

    def get_run_id(self):
        """
        This will get all the run IDs from the database and list them in order of most recent to oldest
        :return:
        """
        # This will get all the unique run_ids and put them into a html that will be used for the dropdown
        self.cursor.execute(f"SELECT DISTINCT RunID FROM {self.table_name} ORDER BY runid DESC ")
        return self.cursor.fetchall()

    def get_graph_data(self, date):
        """
        This will retrieve all the data that matches the selected run ID
        :param date:
        :return:
        """
        print(f"Value: {date}")
        # This will get all the graph data based on the runid that has been selected
        self.cursor.execute(f"SELECT Height, Time, Target Height, Upper_Threshold, Lower_Threshold, Fan_Speed, Kp, Ki, Kd, P_Term, I_Term, D_Term FROM {self.table_name} WHERE runid = {date}")
        return self.cursor.fetchall()




# test = StoreReadings()
# test.create_table()
# test.add_item(1, 20, 2, 22, 18, 6, 7, 8, 9)
# test.remove_item()
# test.get_item()
# test.update_item()
