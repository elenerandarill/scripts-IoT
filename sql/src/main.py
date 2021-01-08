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


print ""
log("Starting application @Python: ", sys.version)

router_id = 1
sensor_id = None
connection = None
cursor = None

try:
    c = ModbusClient(host="192.168.1.168", port=502, auto_open=True)
    connection = mysql.connector.connect(host='serwer2034866.home.pl',
                                         database='32893810_iot',
                                         user='32893810_iot',
                                         password='!Proface123#')

    # collect data from Modbus
    cell_start_index = 0
    nr_of_cells_to_read = 2

    regs = c.read_holding_registers(cell_start_index, nr_of_cells_to_read)
    if not regs:
        print "read error"
    else:
        log("Printed regs: ")
        print regs
        # put each record to database
        for data in regs:
            cell_start_index += 1
            sensor_id = cell_start_index
            sql = "INSERT INTO sensors_data_history (id_router, id_sensor, measurement, time_stamp) VALUES (%s, %s, %s, %s)"
            val = (router_id, sensor_id, data, datetime.today())
            cursor = connection.cursor()
            cursor.execute(sql, val)
            connection.commit()

            # Select specific record from DB if there is any.
            sql = "SELECT id FROM sensors_data_latest WHERE id_router = %s AND id_sensor = %s"
            val = (router_id, sensor_id)
            cursor = connection.cursor()
            cursor.execute(sql, val)
            records = cursor.fetchall()
            # If there is this record - update it, if not - create it.
            if len(records) > 0:
                sql = "UPDATE sensors_data_latest SET measurement = %s, time_stamp = %s WHERE id_router = %s AND id_sensor = %s "
                val = (data, datetime.today(), router_id, sensor_id)
                cursor.execute(sql, val)
                connection.commit()
            else:
                sql = "INSERT INTO sensors_data_latest (id_router, id_sensor, measurement, time_stamp) VALUES (%s, %s, %s, %s)"
                val = (router_id, sensor_id, data, datetime.today())
                cursor.execute(sql, val)
                connection.commit()

    # display data from database
    sql_select_Query = "select * from pomiary"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    log("Total number of rows in pomiary is: ", cursor.rowcount)

    log("Printing each laptop record")
    # from which cell to start displaying
    record_start_index = 0
    # how many records to be displayed in cells
    records_count = 5
    cell_start = 5
    i = 0

    for row in records[record_start_index: records_count]:
        log("id = ", row[0], ", temp = ", row[3], ", bateria  = ", row[4], ", sn  = ", row[2])
        # write_multiple_registers(start_index, [value1, value2, ...])
        if c.write_multiple_registers(cell_start + i, [row[4]]):
            print "write ok"
        else:
            print "write error"
        i += 1

except Error as e:
    log("Error reading data from MySQL table", e)
finally:
    if connection is not None and connection.is_connected():
        connection.close()
        if cursor is not None:
            cursor.close()
        print("MySQL connection is closed")


log("Application stopped")
