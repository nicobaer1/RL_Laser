import pandas as pd
import os
import datetime

def daten_hinzufuegen(df, neue_daten):
    neue_zeile = pd.Series(neue_daten, index=df.columns)
    df = df._append(neue_zeile, ignore_index=True)
    return df

def save_data_point(ID,
                Laserleistung,
                Vorschubgeschwindigkeit,
                Fokusabstand,
                Düsenabstand,
                Düsenduchmesser,
                Gasdruck,
                Schneidgasart,
                Schneidgasmischungsverhältnis,
                Material,
                Materialstärke,
                Abschnittbreite,
                Schnittlänge,
                Abbildungsverhältnis,
                Laserwellenlänge,
                Faserdurchmesser,
                Schnitt_durch,
                Rampenart,
                Rampenstartwert,
                Rampenendwert,
                Verstärkungsfaktor,
                RZ,
                Rm,
                Ra,
                Rq,
                Rp,
                Rv,
                Rsk,
                Rku,
                Sm,
                Sk,
                Maximale_Barthöhe,
                Std_barthöhe,
                Tischposition_Nr,
                reward,
                reward_func,
                Modus,
                Bemerkung
                    ):

    # Netzwerkpfad für die CSV-Datei
    netzwerk_pfad = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\00_Python\00_Python_Programme\01_Datenbank\00_Datenbank_Parameter_CutAIye"
    datei_name = "Datenbank_Parameter_CutAIye.csv"
    dateipfad = os.path.join(netzwerk_pfad, datei_name)

    # Überprüfen, ob die CSV-Datei bereits existiert
    if os.path.exists(dateipfad):
        # Wenn die Datei existiert, lade sie in den DataFrame
        df = pd.read_csv(dateipfad)
    else:
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
    # Aktuelles Datum und Uhrzeit erhalten
    jetzt = datetime.datetime.now()

    # Datum und Uhrzeit in separate Variablen speichern
    Datum = jetzt.date()
    Uhrzeit = jetzt.time()

    # Werte für den Datensatz
    datensatz = [int(ID),
                 float(Laserleistung),
                 float(Vorschubgeschwindigkeit),
                 float(Fokusabstand),
                 float(Düsenabstand),
                 float(Düsenduchmesser),
                 float(Gasdruck),
                 str(Schneidgasart),
                 float(Schneidgasmischungsverhältnis),
                 str(Material),
                 float(Materialstärke),
                 str(Datum),
                 str(Uhrzeit),
                 float(Abschnittbreite),
                 float(Schnittlänge),
                 str(Abbildungsverhältnis),
                 int(Laserwellenlänge),
                 int(Faserdurchmesser),
                 str(Schnitt_durch),
                 str(Rampenart),
                 float(Rampenstartwert),
                 float(Rampenendwert),
                 float(Verstärkungsfaktor),
                 float(RZ),
                 float(Rm),
                 float(Ra),
                 float(Rq),
                 float(Rp),
                 float(Rv),
                 float(Rsk),
                 float(Rku),
                 float(Sm),
                 float(Sk),
                 float(Maximale_Barthöhe),
                 float(Std_barthöhe),
                 int(Tischposition_Nr),
                 float(reward),
                 str(reward_func),
                 str(Modus),
                 str(Bemerkung)
                 ]

    # Hinzufügen von Datensatz
    df = daten_hinzufuegen(df, datensatz)

    # Speichern des aktualisierten DataFrames als CSV-Datei
    df.to_csv(dateipfad, index=False)
    print(f"\nDataFrame wurde als CSV-Datei '{datei_name}' gespeichert.")

