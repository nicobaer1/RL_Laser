import pandas as pd
import os

def daten_hinzufuegen(df, neue_daten):
    neue_zeile = pd.Series(neue_daten, index=df.columns)
    df = df.append(neue_zeile, ignore_index=True)
    return df

# Netzwerkpfad für die CSV-Datei
netzwerk_pfad = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\00_Python\00_Python_Programme\01_Datenbank\00_Datenbank_Parameter_CutAIye"
datei_name = "Datenbank_Parameter_CutAIye.csv"
dateipfad = os.path.join(netzwerk_pfad, datei_name)

# Beispiel für Spaltennamen und leeres DataFrame
spaltennamen = ["ID",
                "Laserleistung [W]",
                "Vorschubgeschwindigkeit [mm/min]",
                "Fokusabstand [mm]",
                "Düsenabstand [mm]",
                "Düsenduchmesser [mm]",
                "Gasdruck[mbar]",
                "Schneidgasart",
                "Schneidgasmischungsverhältnis[%]",
                "Material",
                "Materialstärke[mm]",
                "Datum",
                "Uhrzeit",
                "Abschnittbreite [mm]",
                "Schnittlänge [mm]",
                "Abbildungsverhältnis",
                "Laserwellenlänge [nm]",
                "Faserdurchmesser[µm]",
                "Schnitt durch [Ja/Nein]",
                "Rampenart",
                "Rampenstartwert",
                "Rampenendwert",
                "Verstärkungsfaktor LWM [V]",
                "RZ  (Rauheitstiefe)",
                "Rm (Mittelwert der Rauheitshöhen)",
                "Ra (Arithmetisches Mittel der absoluten Höhenwerte)",
                "Rq (Quadrierter Mittelwert)",
                "Rp (Maximale Rauheit)",
                "Rv (Vertikaler Abstand)",
                "Rsk (Schiefe)",
                "Rku (Kurtosis)",
                "Sm (Kubische Rauheit)",
                "Sk (Kurtosis der Steigung)",
                "Maximale Barthöhe [mm]",
                "Std_barthöhe [mm]",
                "Tischposition_Nr [1-18]",
                "reward",
                "reward_func",
                "Modus",
                "Bemerkung"
                ]
df = pd.DataFrame(columns=spaltennamen)

# Speichern des DataFrames als CSV-Datei
df.to_csv(dateipfad, index=False)
print(f"\nDataFrame wurde als CSV-Datei '{datei_name}' gespeichert.")
