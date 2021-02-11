

class Config:

    # ModbusClient ustawienia:
    host = "192.168.1.168"
    port = 502
    auto_open = True

    # DataBaseModbus ustawienia:
    db_host = 'serwer2034866.home.pl'
    database = '32893810_iot'
    user = '32893810_iot'
    password = '!Proface123#'

    # co ile ma startowac Timer:
    time = 60

    # ------- Odczyt danych z Modbusa -------
    # przykladowe id routera:
    router_id = 1
    # indeks komorki Modbusa, z ktorej startuje odczytywanie danych (pierwsza ma indeks zero!)
    cell_start_index = 0
    # ilosc komorek Modbusa, ktora ma zostac odczytana (np kolejne 5)
    nr_of_cells_to_read = 3

    # ------- Pobieranie danych z tabeli 'nastawy' -------
    # Od ktorej wartosci z tabeli zaczac czytac (pierwszy indeks to zero!)
    record_start_index = 2
    # Ile kolejnych wartosci odczytac
    records_count = 5
    # Od ktorej komorki Modbusa zaczac wyswietlac dane
    current_cell_idx = 5


