import csv
import numpy as np

file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\00_Python\00_Python_Programme\00_Automatisierung\Reinforcement_learning_main\action\action.txt"
import csv
import numpy as np

def read_action():
    try:
        # CSV-Datei öffnen und den Wert lesen
        with open(file_path, "r", newline="") as f:
            reader = csv.reader(f)
            # Die erste Zeile der CSV-Datei lesen und in eine Liste umwandeln
            row = next(reader)
            # Werte aus der Liste extrahieren und in ein Array konvertieren
            action_array = np.array([np.float(val) for val in row]) if row else None

            return action_array
    except Exception as e:
        print("Fehler beim Lesen der CSV-Datei:", e)
        return None
test = read_action()
print("Gelesene Werte als Array von Floats:", test)
