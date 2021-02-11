# scripts-IoT
scripts for IoT Modbus

## Konfiguracja projektu:

Na routerze są moduły: `URRouterInfo`, `URMessageChannel`, etc.
Na Windowsie ich nie ma, więc jest zrobiony symulator.
Symulator znajduje się w innym katalogu niż projekt (tutaj: `router_sim`).
Z tego powodu PyCharm przy próbie **import URRouterInfo** wyrzuca błąd **Unresolved reference**.
Można to naprawić przez oznaczenie katalogu z kodami symulatora w PyCharmie jako *źródłowy*

>>> trzeba na katalog `router_sim` kliknąć **PPM** i wybrać `Mark Directory as` -> `Sources root`.


```
main.py:
```

- najpierw wykonuje się odczyt określonej liczby komórek (`nr_of_cells_to_read`) z ekranu i jeśli poszło dobrze, 
to są one wypisywane w konsoli i zapisywane do bazy danych `sensors_data_history`, przy okazji kod nadpisuje pomiary
w bazie danych `sensors_data_latest` - tu są najświeższe pomiary dla każdego czujnika;

- potem wykonuje się wypisywanie wybranych danych z bazy `sensors_data_history` na komówki Modbusa zaczynając od `current_cell_idx`
(można to zastąpić bazą `sensors_data_latest`, póki co użyłam `history`, żeby móc wyświetlać inne rekody, bo pobierałabym
dane do `latest` i wyświetlała dokładnie to samo po chwili...);

- zastosowałam `Timer` i *main.py* odpala się co **60sek**;


```
utils.py:
```

- funkcja to wypisywania logów na ekranu;


```
database_modbus_cls.py:
```

- funkcje obsługujące rekordy bazy danych;


```
measurement_record_cls.py:
```

- klasa obiektu MeasurementRecord.
