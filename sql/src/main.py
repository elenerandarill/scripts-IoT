import socket
if not hasattr(socket, 'inet_pton'):
    import win_inet_pton
import sys

from database_modbus_cls import DataBaseModbus
from measurement_record_cls import MeasurementRecord
from utils import log
from config import Config

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
        print ""
        log(">>> in timerHandle()")
        # Show cellular status
        log(URRouterInfo.get_cellular_status())
        # Run main script.
        log("before main")
        main()
        log("after main")
        # Add timer and start it after 5 seconds
        self.startTimer()
        log("after start timer")


def main():
    router_id = Config.router_id
    my_db = None

    try:
        # ------- Reading from the screen -------
        iot_screen = ModbusClient(Config.host, Config.port, Config.auto_open)
        my_db = DataBaseModbus(Config.db_host, Config.database, Config.user, Config.password)

        cell_start_index = Config.cell_start_index
        nr_of_cells_to_read = Config.nr_of_cells_to_read

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

        # ------- Printing data from db onto screen -------
        # From which record in DB (INDEXED FROM 0) to start reading data
        record_start_index = Config.record_start_index
        # How many records to be read
        records_count = Config.records_count
        # Cell index starting to display values
        current_cell_idx = Config.current_cell_idx

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
            # print("MySQL connection is closed")

    log("Application stopped")


if __name__ == '__main__':
    print ""
    log("Starting app @", sys.version)
    # instantiates a testTimer,set timer trigger time
    timer = TestTimer(Config.time)
    # start event loop
    timer.start()





