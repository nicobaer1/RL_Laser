import pandas as pd
import os

# Netzwerkpfad für die CSV-Datei
netzwerk_pfad = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\00_Python\00_Python_Programme\01_Datenbank\00_Datenbank_Parameter_CutAIye"
datei_name = "Datenbank_Parameter_CutAIye.csv"
dateipfad = os.path.join(netzwerk_pfad, datei_name)
# Überprüfen, ob die CSV-Datei existiert
if os.path.exists(dateipfad):
    # CSV-Datei laden
    df = pd.read_csv(dateipfad)

    # Kopf der CSV-Datei anzeigen
    print(df.head())
    # Kopf der CSV-Datei anzeigen
    print(df[["ID", "reward"]])
    min_reward_index = df['reward'].idxmin()
    min_reward_entry = df.loc[min_reward_index]
    print(min_reward_entry[['ID', 'reward']])
    max_reward_index = df['reward'].idxmax()
    max_reward_entry = df.loc[max_reward_index]
    print(max_reward_entry[['ID', 'reward']])

    """print(df["Laserleistung"])"""
    print(df["Schnitt durch [Ja/Nein]"])
else:
    print("Die CSV-Datei existiert nicht.")
