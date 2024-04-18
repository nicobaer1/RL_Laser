import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Lade die Parameterkombinationen aus der Textdatei
file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Parameterraum\50.txt"

# Laden der Daten aus der Datei
try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        data = [list(map(float, line.strip().split())) for line in lines]
except FileNotFoundError:
    print(f"Die Datei '{file_path}' wurde nicht gefunden.")
    exit()
except Exception as e:
    print(f"Fehler beim Laden der Datei '{file_path}': {e}")
    exit()

# Überprüfen, ob die Daten 5 Werte pro Zeile enthalten
for i, row in enumerate(data):
    if len(row) != 5:
        print(f"Fehler in Zeile {i+1}: Jede Zeile muss genau 5 Werte enthalten.")
        exit()

# Konvertieren der Daten in ein Pandas DataFrame
df = pd.DataFrame(data, columns=["Laserleistung", "Gasdruck", "Vorschub", "Düsenabstand", "Fokuslage"])

# Visualisierung der Daten in einem 3D-Diagramm
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Parameter für Position, Farbe und Größe festlegen
x = df["Laserleistung"]
y = df["Gasdruck"]
z = df["Vorschub"]
c = df["Fokuslage"]  # Farbe der Punkte basierend auf einem anderen Parameter
s = df["Düsenabstand"] * 10  # Größe der Punkte basierend auf dem fünften Parameter (multipliziert mit 10 für die Sichtbarkeit)
values = df["Düsenabstand"]
# Punkte im 3D-Diagramm plotten
scatter = ax.scatter(x, y, z, c=c, cmap='viridis', s=s)

# Farblegende hinzufügen
cbar = plt.colorbar(scatter,orientation='horizontal')
cbar.set_label("Fokuslage")

# Legende für die Punktgrößen

legend = ax.legend(*scatter.legend_elements(prop='sizes', labels=values), title='Punktgröße', loc='center left', bbox_to_anchor=(1.2, 0.5))

ax.add_artist(legend)

# Achsenbeschriftungen
ax.set_xlabel('Laserleistung')
ax.set_ylabel('Gasdruck')
ax.set_zlabel('Vorschub')

plt.show()
