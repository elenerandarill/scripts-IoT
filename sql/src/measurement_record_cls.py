from datetime import datetime


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

