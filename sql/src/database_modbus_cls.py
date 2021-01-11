import socket
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton

from utils import log
from measurement_record_cls import MeasurementRecord

import mysql.connector


class DataBaseModbus:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = self.make_connection()

    def make_connection(self):
        conn = mysql.connector.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        if conn:
            log("Connection established.")
            return conn
        else:
            raise Exception("Connection failed.")

    def close_connection(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            log("MySQL connection is closed")

    def insert_measurement_history(self, m):
        sql_operation = "INSERT INTO sensors_data_history (id_router, id_sensor, amount, time_stamp) VALUES (%s, %s, %s, %s)"
        values = (m.router_id, m.sensor_id, m.amount, m.time_stamp)
        mycursor = self.connection.cursor()
        mycursor.execute(sql_operation, values)
        self.connection.commit()
        log("Measurement saved: ", m)
        mycursor.close()

    def has_latest_measurement(self, rout_id, sens_id):
        sql_operation = "SELECT id FROM sensors_data_latest WHERE id_router = %s AND id_sensor = %s"
        values = (rout_id, sens_id)
        mycursor = self.connection.cursor()
        mycursor.execute(sql_operation, values)
        result = mycursor.fetchall()
        mycursor.close()
        # Returns a list.
        return result

    def update_latest_measurement(self, m):
        sql_operation = "UPDATE sensors_data_latest SET amount = %s, time_stamp = %s WHERE id_router = %s AND id_sensor = %s "
        values = (m.amount, m.time_stamp, m.router_id, m.sensor_id)
        mycursor = self.connection.cursor()
        mycursor.execute(sql_operation, values)
        self.connection.commit()
        mycursor.close()

    def insert_latest_measurement(self, m):
        sql_operation = "INSERT INTO sensors_data_latest (id_router, id_sensor, amount, time_stamp) VALUES (%s, %s, %s, %s)"
        values = (m.router_id, m.sensor_id, m.amount, m.time_stamp)
        mycursor = self.connection.cursor()
        mycursor.execute(sql_operation, values)
        self.connection.commit()
        mycursor.close()

    def insert_measurement(self, measurement):
        self.insert_measurement_history(measurement)

        records = self.has_latest_measurement(measurement.router_id, measurement.sensor_id)
        if len(records) > 0:
            self.update_latest_measurement(measurement)
        else:
            self.insert_latest_measurement(measurement)

    # Display selected DB data onto Modbus screen
    def get_history_measurements(self, record_start_index, records_count):
        sql_operation = "SELECT * FROM sensors_data_history LIMIT %s OFFSET %s"
        values = (records_count, record_start_index)
        mycursor = self.connection.cursor()
        mycursor.execute(sql_operation, values)
        results = mycursor.fetchall()
        results_objects = []
        for r in results:
            m = MeasurementRecord(r[1], r[2], r[3], time_stamp=r[4], m_id=r[0])
            results_objects.append(m)
        mycursor.close()
        return results_objects
