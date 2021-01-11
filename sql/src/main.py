import socket
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton

import sys
import os
import time
from datetime import datetime

from database_modbus_cls import DataBaseModbus
from measurement_record_cls import MeasurementRecord
from utils import log

import mysql.connector
from mysql.connector import Error
from pyModbusTCP.client import ModbusClient
import URRouterInfo
from URMessageChannel import TimerEvtHandle, init_base


class TestTimer(TimerEvtHandle):
    def __init__(self, time):
        # init an event base
        self.base = init_base()
        # super(TestTimer, self).__init__(self.base, time)
        TimerEvtHandle.__init__(self, self.base, time)

    def timerHandle(self, evt, userdata):
        # Show cellular status
        log(URRouterInfo.get_cellular_status())
        # Run main script.
        log("before main")
        main()
        log("after main")
        # Add timer and start it after 5 seconds
        self.startTimer()

def main():
    print ""
    log("Starting app @", sys.version)

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


if __name__ == '__main__':
    # instantiates a testTimer,set timer trigger time
    timer = TestTimer(60)
    # start event loop
    timer.start()





