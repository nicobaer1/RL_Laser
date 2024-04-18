import csv
import os

def create_csv(folder, filename):
    headers = ["ID", "Datum", "Uhrzeit", "Laserleistung [W]", "Gasdruck [mbar]", "Vorschubgeschwindigkeit [mm/min]",
               "Düsenabstand [mm]", "Fokusabstand [mm]", "RZ", "Rm", "Ra", "Rq", "Rp", "Rv", "Rsk", "Rku",
               "Sm", "Sk", "Maximale Barthöhe [mm]", "Std_barthöhe [mm]", "Material", "Materialstärke [mm]",
               "Tischposition_Nr [1-18]",  "Düsendurchmesser [mm]", "Schneidgasart",
               "Abschnittbreite [mm]", "Schnittlänge [mm]", "Abbilungsverhältnis", "Laserwellenlänge [nm]",
               "Faserdurchmesser [μm]", "Schnitt durch [Ja/Nein]", "Verstärkungsfaktor LWM [V]"]

    full_path = os.path.join(folder, filename)

    with open(full_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

# Specify the folder and filename
file_folder = r'\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\RL_3D_Punktewolke'
csv_filename = "Datenbank_Laserschneiden.csv"

# Example call
create_csv(file_folder, csv_filename)
q