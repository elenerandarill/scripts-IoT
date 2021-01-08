import socket
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton

import sys
import os
import time
from datetime import datetime

import mysql.connector
from mysql.connector import Error
from pyModbusTCP.client import ModbusClient


def log(*args):
    # print("got log() ", args)
    now = datetime.now()
    now_formatted = now.strftime("%H:%M:%S")
    args2 = [now_formatted, " "]
    args2.extend(args)
    print "".join(map(str, args2))




class MeasurementRecord:
    def __init__(self, router_id, sensor_id, amount, time_stamp=None, m_id=None):
        self.m_id = m_id
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.amount = amount
        if time_stamp:
            self.time_stamp = time_stamp
        else:
            self.time_stamp = datetime.today()

    def __repr__(self):
        return "MeasurementRecord(id: %s, rid: %s, sid: %s, amount: %s, timestamp: %s)" % (self.m_id, self.router_id, self.sensor_id, self.amount, self.time_stamp)


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


######
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


#########################################

def main():
    print ""
    log("Starting application @Python: ", sys.version)

    router_id = 1
    my_db = None

    try:
        iot_screen = ModbusClient(host="192.168.1.168", port=502, auto_open=True)
        my_db = DataBaseModbus('serwer2034866.home.pl', '32893810_iot', '32893810_iot', '!Proface123#')

        cell_start_index = 0
        nr_of_cells_to_read = 3

        regs = iot_screen.read_holding_registers(cell_start_index, nr_of_cells_to_read)
        if not regs:
            log("read error")
        else:
            log("Printed regs: ")
            print regs
            # put each record to database
            for data in regs:
                cell_start_index += 1
                sensor_id = cell_start_index
                measurement = MeasurementRecord(router_id, sensor_id, data)
                my_db.insert_measurement(measurement)

        log("Printing each DB record:")

        # From which record (INDEXED FROM 0) to start reading
        record_start_index = 2
        # How many records to be read
        records_count = 5
        # Cell index starting to display values
        current_cell_idx = 5

        records = my_db.get_history_measurements(record_start_index, records_count)
        # Display data onto Modbus
        for r in records:
            log(r)
            # write_multiple_registers(start_index, [value1, value2, ...])
            if not iot_screen.write_multiple_registers(current_cell_idx, [r.amount]):
                log("write error")
            current_cell_idx += 1

    except Error as e:
        log("Error reading data from MySQL table", e)
    finally:
        if my_db:
            my_db.close_connection()
            print("MySQL connection is closed")

    log("Application stopped")


main()
