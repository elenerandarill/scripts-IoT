# For creating Table

# Table with measurements history data
CREATE TABLE sensors_data_history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_router INTEGER,
    id_sensor INTEGER,
    amount FLOAT,
    time_stamp DATETIME
);

# Table with latest measurements for each sensor
CREATE TABLE sensors_data_latest (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_router INTEGER,
    id_sensor INTEGER,
    amount FLOAT,
    time_stamp DATETIME
);