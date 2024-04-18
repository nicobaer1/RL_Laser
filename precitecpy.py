import csv
import numpy as np
import matplotlib.pyplot as plt

# CSV-Datei einlesen und Kopf anzeigen
def obs(Versuchsummer):
    #file_path = r'\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\LWM CutAIye\\'# Pfad zur CSV-Datei
    file_path = r'\\Te31149\d\Export\MeasurementExport\\'
    #\\Te31149\d\Export\MeasurementExport
    #USER: User
    #Passwort: User oder admin

    filename = str(Versuchsummer)+'.csv'  # Name der CSV-Datei
    print("filename",filename)
    full_path = file_path + filename  # Vollständiger Pfad zur CSV-Datei

    # Bereich der Zeilen, die angezeigt werden sollen
    start_row = 1000
    end_row = 499010

    # Zeit- und P-Raw-Daten initialisieren
    time = []
    p_raw = []
    t_raw = []
    r_raw = []

    # CSV-Datei öffnen und Daten extrahieren
    with open(full_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader)  # Überspringen der Kopfzeile
        for i, row in enumerate(csvreader):
            if i < start_row:
                continue
            if i > end_row:
                break
            # Extrahieren von Zeit- und P-Raw-Werten
            time.append(float(row[1].replace('.', '').replace(',', '.')))  # Die zweite Spalte (Index 1) enthält Time-Werte
            p_raw.append(float(row[2].replace('.', '').replace(',', '.')))  # Die dritte Spalte (Index 2) enthält P-Raw-Werte
            t_raw.append(float(row[3].replace('.', '').replace(',', '.')))  # Die dritte Spalte (Index 2) enthält P-Raw-Werte
            r_raw.append(float(row[4].replace('.', '').replace(',', '.')))  # Die dritte Spalte (Index 2) enthält P-Raw-Werte
    # Ein 2D-NumPy-Array erstellen, wobei jede Spalte die entsprechenden Werte aus p_raw, t_raw und r_raw enthält
    matrix = np.array([p_raw, t_raw,r_raw]).T  # .T wird verwendet, um die Matrix zu transponieren, so dass die Zeilen in die Spalten umgewandelt werden


    # Plot von Time gegen P-Raw, T-Raw und R-Raw
    plt.plot(time, p_raw, label='P-Raw', linestyle='-')
    plt.plot(time, t_raw, label='T-Raw', linestyle='-')
    plt.plot(time, r_raw, label='R-Raw', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Raw Values')
    plt.title('Plot von Time gegen P-Raw, T-Raw und R-Raw')
    plt.grid(True)
    plt.legend()
    plt.show()
    return matrix


obs(3125)