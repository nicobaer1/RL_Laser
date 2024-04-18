import pandas as pd
import numpy as np
import os
from sobol_seq import i4_sobol_generate


# Funktion zum Laden der Parameterkombinationen aus der Tabelle
def load_parameter_table(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Verarbeiten Sie die Zeilen der Datei und extrahieren Sie die Parameterkombinationen
        parameter_list = []
        for line in lines:
            parameters = line.strip().split(" ")  # Annahme: Die Parameter sind durch Leerzeichen getrennt
            if len(parameters) == 5:  # Überprüfen Sie, ob die Anzahl der Parameter korrekt ist
                parameter_list.append(parameters)
            else:
                print(f"Fehlerhafte Zeile: {line.strip()}")

        return parameter_list
    except FileNotFoundError:
        print(f"Die Datei '{file_path}' wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Laden der Datei '{file_path}': {e}")
        return None


# Funktion zum Extrahieren und Entfernen einer Parameterkombination aus der Liste
def extract_and_remove_combination(parameter_list, sobol_sequence):
    if len(parameter_list) == 0:
        print("Die Parameterliste ist leer. Es wurden alle Kombinationen extrahiert.")
        return None

    # Generieren Sie den Index basierend auf der Sobol-Sequenz
    index = int(sobol_sequence[0] * len(parameter_list))

    # Extrahieren der entsprechenden Parameterkombination
    combination = parameter_list[index]

    # Entfernen der ausgewählten Parameterkombination aus der Liste
    del parameter_list[index]

    return combination


def save_extracted_parameters(file_path, extracted_parameters):
    try:
        with open(file_path, "a", encoding="latin1") as file:
            for combination in extracted_parameters:
                line = " ".join(map(str, combination)) + "\n"
                file.write(line)
        print(f"Die extrahierten Parameter wurden erfolgreich in '{file_path}' gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der extrahierten Parameter in '{file_path}': {e}")


# Speicherort der Parameterdatei
file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Parameterraum\parameter_kombinationen.txt"
extracted_parameters_file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Parameterraum\parameter_kombinationen_geschnitten.txt"

# Laden der Parameterkombinationen aus der Tabelle
# Laden der Parameterkombinationen aus der Tabelle
parameter_list = load_parameter_table(file_path)

if parameter_list:
    # Generieren einer Sobol-Sequenz für den Index
    sobol_sequence = i4_sobol_generate(5, len(parameter_list))

    # Extrahieren und Entfernen einer Parameterkombination
    combination = extract_and_remove_combination(parameter_list, sobol_sequence)
    if combination:
        print("Extrahierte Parameterkombination:", combination)

        # Speichern der extrahierten Parameter
        save_extracted_parameters(extracted_parameters_file_path, [combination])

        # Aktualisieren der Parameterdatei, um die extrahierte Kombination zu entfernen
        df = pd.DataFrame(parameter_list)
        df.to_csv(file_path, sep=" ", index=False, header=False)

        print("Die Parameterkombination wurde aus der Liste entfernt und die Parameterdatei wurde aktualisiert.")
    else:
        print("Keine Parameterkombinationen mehr in der Liste.")
else:
    print("Fehler beim Laden der Parameterkombinationen aus der Tabelle.")