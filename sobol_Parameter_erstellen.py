import numpy as np
from sobol_seq import i4_sobol_generate

# Definiere die Grenzen für jeden Parameter
parameter_ranges = {
    "Laserleistung": (2000, 8000),
    "Gasdruck": (8000, 18000),
    "Vorschub": (1000, 5000),
    "Düsenabstand": (1, 3),
    "Fokusabstand": (-10, 3)
}

# Definiere die Anzahl der gewünschten Kombinationen
num_combinations = 50

# Erzeuge eine Sobol-Sequenz für die Anzahl der Parameterdimensionen (5)
sobol_sequence = i4_sobol_generate(5, num_combinations)

# Benutzer eingeben
file_name = input("Bitte geben Sie den Dateinamen ein (ohne Erweiterung): ")

# Pfade definieren
directory_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Parameterraum"
new_file_path = fr"{directory_path}\{file_name}.txt"

# Erzeuge leere Listen, um die generierten Kombinationen zu speichern
parameter_combinations = []

# Iteriere über die Sobol-Sequenz und skaliere die Werte entsprechend den Parameterranges
for seq in sobol_sequence:
    combination = []
    for i, (param, (low, high)) in enumerate(parameter_ranges.items()):
        # Skaliere den Sobol-Wert auf den Parameterraum und runde auf zwei Nachkommastellen
        scaled_value = round(low + seq[i] * (high - low), 2)
        combination.append(scaled_value)
    parameter_combinations.append(combination)

# Speichere die Liste der Parameterkombinationen in der neuen Textdatei
with open(new_file_path, "w") as file:
    for combination in parameter_combinations:
        file.write(" ".join(map(str, combination)) + "\n")

print(f"Die Liste der Parameterkombinationen wurde erfolgreich unter '{new_file_path}' gespeichert.")
