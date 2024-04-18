import csv
import numpy as np
import matplotlib.pyplot as plt
import  time
def linear_interpolation(x, y, new_points):
    new_x = np.linspace(min(x), max(x), new_points)
    new_y = np.interp(new_x, x, y)
    return new_x, new_y

def process_data(file_path, start_row, end_row, threshold_high, num_points):
    # Zeit- und Rohdaten initialisieren
    time = []
    p_raw = []
    t_raw = []
    r_raw = []

    # CSV-Datei öffnen und Daten extrahieren
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader)  # Überspringen der Kopfzeile
        for i, row in enumerate(csvreader):
            if i < start_row:
                continue
            if i > end_row:
                break
            # Extrahieren von Zeit-, P-Raw-, T-Raw- und R-Raw-Werten
            time.append(float(row[1].replace('.', '').replace(',', '.')))
            p_raw.append(float(row[2].replace('.', '').replace(',', '.')))
            t_raw.append(float(row[3].replace('.', '').replace(',', '.')))
            r_raw.append(float(row[4].replace('.', '').replace(',', '.')))

    # Zeitpunkte für P-Raw, T-Raw und R-Raw, an denen der Schwellenwert überschritten wird
    trigger_time_p_raw = None

    # Hysterese auf die P-Raw-Daten anwenden und Zeitpunkt des Trigger-Übergangs finden
    for i, value in enumerate(p_raw):
        if trigger_time_p_raw is None and value > threshold_high:
            trigger_time_p_raw = i
            break

    # Plot nur, wenn der Trigger von P-Raw ausgelöst wird
    if trigger_time_p_raw is not None:
        # Zeitindex des Triggers
        trigger_index = trigger_time_p_raw

        # Daten für die nächsten 1000 Werte nach dem Trigger erfassen
        time_trigger = time[trigger_index + 20000:trigger_index + 20 + num_points]
        p_raw_trigger = p_raw[trigger_index + 20000:trigger_index + 20 + num_points]
        t_raw_trigger = t_raw[trigger_index + 20000:trigger_index + 20 + num_points]
        r_raw_trigger = r_raw[trigger_index + 20000:trigger_index + 20 + num_points]

        # Lineare Interpolation auf die drei Signale anwenden
        new_points = 1000
        p_raw_interp_x, p_raw_interp_y = linear_interpolation(time_trigger, p_raw_trigger, new_points)
        t_raw_interp_x, t_raw_interp_y = linear_interpolation(time_trigger, t_raw_trigger, new_points)
        r_raw_interp_x, r_raw_interp_y = linear_interpolation(time_trigger, r_raw_trigger, new_points)

        # Plot der interpolierten Daten
        plt.plot(p_raw_interp_x, p_raw_interp_y, label='Interpolated P-Raw', linestyle='-')
        plt.plot(t_raw_interp_x, t_raw_interp_y, label='Interpolated T-Raw', linestyle='-')
        plt.plot(r_raw_interp_x, r_raw_interp_y, label='Interpolated R-Raw', linestyle='-')

        # Plot der Rohdaten
        plt.plot(time_trigger, p_raw_trigger, label='P-Raw', linestyle='-')
        plt.plot(time_trigger, t_raw_trigger, label='T-Raw', linestyle='-')
        plt.plot(time_trigger, r_raw_trigger, label='R-Raw', linestyle='-')

        plt.xlabel('Time')
        plt.ylabel('Raw Values')
        plt.title('Plot von Time gegen P-Raw, T-Raw und R-Raw nach P-Raw Schmitt-Trigger')
        plt.grid(True)
        plt.legend()
        plt.pause(1)  # Diagramm bleibt für 3 Sekunden offen
        #plt.close()  # Diagramm schließen"""
        plt.show()
        # Erstellen der Matrix
        matrix = np.array([r_raw_interp_y, p_raw_interp_y, t_raw_interp_y]).T
        #print("Matrix shape:", matrix.shape)
        return matrix

    else:
        print("Trigger-Schwellenwert wurde nicht erreicht.")

# Test der Funktion
def obs(ID):
    import os

    file_path = r'\\Te31149\d\Export\MeasurementExport\\'  # Pfad zum Verzeichnis, in dem die CSV-Datei liegt
    filename = str(ID) + '.csv'  # Name der CSV-Datei
    full_path = os.path.join(file_path, filename)  # Vollständiger Pfad zur CSV-Datei

    while not os.path.isfile(full_path):  # Solange die Datei nicht gefunden wurde
        print("Die Datei fehlt im angegebenen Verzeichnis.")
        user_input = input("Wurde die Datei abgespeichert? (ja/nein): ").lower()
        if user_input == 'ja':
            # Warten, bevor erneut überprüft wird, ob die Datei vorhanden ist
            print("Die Datei wird erneut überprüft...")
            time.sleep(5)  # Wartezeit in Sekunden
        elif user_input == 'nein':
            print("Bitte speichern Sie die Datei ab und starten Sie das Programm erneut.")
            exit()  # Das Programm beenden, wenn der Benutzer angibt, dass die Datei nicht abgespeichert wurde
        else:
            print("Ungültige Eingabe. Bitte antworten Sie mit 'ja' oder 'nein'.")

    print("Die Datei wurde im angegebenen Verzeichnis gefunden.")

    start_row = 100
    end_row = 498011
    threshold_high = 1500
    num_points = 25000

    return process_data(full_path, start_row, end_row, threshold_high, num_points)

obs(3707)