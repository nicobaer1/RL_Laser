'''
# Aktionsraum definieren
Laserleistung_low, Laserleistung_high = 2000, 8000
Gasdruck_low, Gasdruck_high = 8000, 18000
Vorschub_low, Vorschub_high = 1000, 5000
Düsenabstand_low, Düsenabstand_high = 1, 3
Fokusabstand_low, Fokusabstand_high = -10, 3

def parameter_generator():
    for laser_leistung in range(Laserleistung_low, Laserleistung_high + 1, 500):
        for gasdruck in range(Gasdruck_low, Gasdruck_high + 1, 2000):
            for vorschub in range(Vorschub_low, Vorschub_high + 1, 1000):
                for düsenabstand in range(Düsenabstand_low, Düsenabstand_high + 1):
                    for fokusabstand in range(Fokusabstand_low, Fokusabstand_high + 1):
                        yield laser_leistung, gasdruck, vorschub, düsenabstand, fokusabstand
# Zähler für die Anzahl der Kombinationen
combination_count = 0

# Testen der Funktion
for parameter_set in parameter_generator():
    print(parameter_set)
    combination_count += 1

print("combination_count",combination_count)
'''
# Aktionsraum definieren
Laserleistung_low, Laserleistung_high = 2000, 8000
Gasdruck_low, Gasdruck_high = 8000, 18000
Vorschub_low, Vorschub_high = 1000, 5000
Düsenabstand_low, Düsenabstand_high = 1, 3
Fokusabstand_low, Fokusabstand_high = -10, 3


def parameter_generator():
    for laser_leistung in range(Laserleistung_low, Laserleistung_high + 1, 500):
        for gasdruck in range(Gasdruck_low, Gasdruck_high + 1, 2000):
            for vorschub in range(Vorschub_low, Vorschub_high + 1, 1000):
                for düsenabstand in range(Düsenabstand_low, Düsenabstand_high + 1):
                    for fokusabstand in range(Fokusabstand_low, Fokusabstand_high + 1):
                        yield laser_leistung, gasdruck, vorschub, düsenabstand, fokusabstand


# Speicherort der Datei
speicherort = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Parameterraum\parameter_kombinationen.txt"

# Öffnen der Datei zum Schreiben
with open(speicherort, "w") as file:
    # Schreiben der Überschriften
    file.write("# Laserleistung Gasdruck Vorschub Düsenabstand Fokusabstand\n")

    # Iterieren über die Parameter und Schreiben in die Datei
    for parameter_set in parameter_generator():
        # Konvertieren der Parameter in eine Zeichenkette und Schreiben in die Datei
        parameter_string = " ".join(map(str, parameter_set)) + "\n"
        file.write(parameter_string)

print(f"Die Parameter wurden erfolgreich in die Datei '{speicherort}' gespeichert.")
