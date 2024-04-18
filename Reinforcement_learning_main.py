# import pyads
import time
import beckhoffpy
import trumpfpy
import numpy as np
import IDSpy
import Save_data_point_to_a_CSV_file
import mircoepsilonpy
from trumpfpy import G_Code_parameterübergabe
from mircoepsilonpy import reward
beckhoffpy.Trigger_TLC_Beleuchtung_EIN()
beckhoffpy.ventilator()
modus = "RL" #Modus (RL, OB oder Manuel)
count = 0
count_Fokusabstand = 0
count_Düsenabstand = 0
ID = input("Geben die aktuelle ID des LWMs ein : ")
ID = int(ID) + 1
x_start = None

x_start = 2325
y_start = 1232 - (5*20)
z_start = 255.517
x_end = 140
y_end = 0
z_end = 0
Schneidgasart = "Stickstoff"

#beckhoffpy.MAIN_Positionswechsel_Tisch(1)<
while True:
    user_input = input("Möchten Sie fortfahren? (Ja/Nein): ")
    if user_input.lower() == "ja":
        print("Fortfahren...")
        # Fügen Sie hier den Code ein, den Sie ausführen möchten

    elif user_input.lower() == "nein":
        print("Programm beendet.")
        break  # Die Schleife wird beendet
    else:
        print("Ungültige Eingabe. Bitte geben Sie 'Ja' oder 'Nein' ein.")
        # Die Schleife wird fortgesetzt und der Benutzer wird erneut nach einer Eingabe gefragt
    count += 1
    count_Fokusabstand +=1
    count_Düsenabstand+=1

    if count % 18 == 0:  # Wenn die Anzahl der Versuche durch 18 teilbar ist
        y_start -= 5  # y_start um 5 verringern

    beckhoffpy.delete_folder_contents()
    # Benutzereingabe abfragen und in einer Variable speichern    
    #beckhoffpy.MAIN_Positionswechsel_Tisch(1)
    beckhoffpy.GVL_Achse(4, 0)
    beckhoffpy.GVL_Achse(3, 0)
    beckhoffpy.Trigger_TLC_Beleuchtung_EIN()
    print("\033[91mAktuelle ID: {}\033[00m".format(ID))

    # Überprüfung der Eingabe
    if modus == "RL":
        # Load the array from the text file
        Laserleistung, Gasdruck, Vorschub, Düsenabstand, Fokusabstand = np.loadtxt('action_array.txt')
    elif modus == "OB":
        pass  # Fügen Sie hier Ihren Code für den "OB"-Modus ein
    elif modus == "Manuel":
        Laserleistung = 4500
        Gasdruck = 12000
        Vorschub = 2500
        Düsenabstand = 3 + ((count_Düsenabstand - 1) // 27)
        Fokusabstand = -17 + (count_Fokusabstand % 27)
        print("Fokusabstand",Fokusabstand)
        print("Count",count)
    elif modus =="Liste":
        print("")


    else:
        print("Ungültige Eingabe. Bitte gib RL, OB, Manuel oder 'exit' ein.")
        exit()

    # Anzeigen des aktuellen Modus
    print("Aktueller Modus:", modus)

    # Formatieren und Ausgeben der Variablen
    print("\033[94mLaserleistung:\033[0m", "\033[91m", Laserleistung, "\033[0m",
          "\033[94mGasdruck:\033[0m", "\033[91m", Gasdruck, "\033[0m",
          "\033[94mVorschub:\033[0m", "\033[91m", Vorschub, "\033[0m",
          "\033[94mDüsenabstand:\033[0m", "\033[91m", Düsenabstand, "\033[0m",
          "\033[94mFokusabstand:\033[0m", "\033[91m", Fokusabstand, "\033[0m")


    beckhoffpy.düsenabstand(Düsenabstand)
    beckhoffpy.fokusabstand(Fokusabstand)

    G_Code_parameterübergabe(Laserleistung=Laserleistung,
                                      Gasdruck=Gasdruck,
                                      Vorschub=Vorschub,
                                      x_start=x_start,
                                      y_start=y_start,
                                      z_start=z_start,
                                      x_end=x_end,
                                      y_end=y_end,
                                      z_end=z_end,
                                      Schneidgasart=Schneidgasart)


    #beckhoffpy.MAIN_Positionswechsel_Tisch(1)
    time.sleep(2)
    trumpfpy.TLC_start_cutting()
    time.sleep(3)
    trumpfpy.TLC_end_cutting()
    time.sleep(15)
    beckhoffpy.MAIN_Positionswechsel_Tisch(3)
    beckhoffpy.Trigger_TLC_Beleuchtung_AUS()
    beckhoffpy.IDS_Kamera_automatisch(y_start,ID)
    beckhoffpy.Trigger_TLC_Beleuchtung_EIN()
    beckhoffpy.MAIN_Positionswechsel_Tisch(2)
    beckhoffpy.Trigger_TLC_Beleuchtung_AUS()
    beckhoffpy.Sensor3D_automatisch(y_start,ID)
    beckhoffpy.Trigger_TLC_Beleuchtung_EIN()


    def meine_funktion(Laserleistung = Laserleistung, Gasdruck = Gasdruck, Vorschub = Vorschub, Düsenabstand= Düsenabstand, Fokusabstand=Fokusabstand):

        # Formatieren und Ausgeben der Variablen
        print("\033[94mLaserleistung:\033[0m", "\033[91m", Laserleistung, "\033[0m",
              "\033[94mGasdruck:\033[0m", "\033[91m", Gasdruck, "\033[0m",
              "\033[94mVorschub:\033[0m", "\033[91m", Vorschub, "\033[0m",
              "\033[94mDüsenabstand:\033[0m", "\033[91m", Düsenabstand, "\033[0m",
              "\033[94mFokusabstand:\033[0m", "\033[91m", Fokusabstand, "\033[0m")



    #Parameter sammeln
    #Confi
    Düsendurchmesser = 3 #mm
    Schneidgasart = "Stickstoff"
    Scneidgasmischungsverhältnis = 0
    Material = "Edelstahl"
    Materialstärke = 5 # mm
    Abschnittbreite = 5 # mm
    Schnittlänge = 80 # mm
    Abbildungsverhältnis = "1:1,5"
    Laserewellenlänge = 1030
    Faserdurchmesser = 100
    Rampenart = "-"
    Rampenstartwert =0
    Rampenendwert = 0
    Verstärkungsfaktor_LWM = 10
    Tischposition= 0
    Modus = modus
    Bemerkung = "keine"

    'Schnittparameter'
    # Benutzereingabe für die Spalte "Schnitt durch [Ja/Nein]"
    schnitt_durch = input("Handelt es sich um einen Schnitt durch? (Ja/Nein): ").strip().capitalize()

    # Überprüfen, ob die Eingabe gültig ist
    while schnitt_durch not in ['Ja', 'Nein']:
        print("Ungültige Eingabe. Bitte geben Sie 'Ja' oder 'Nein' ein.")
        schnitt_durch = input("Handelt es sich um einen Schnitt durch? (Ja/Nein): ").strip().capitalize()

    reward, RZ, RM, RA, Rq,Rp, Rv,Rsk, Rku,Sm, Sk , max_y_range,std_deviation, reward_func = mircoepsilonpy.reward(ID)
    Save_data_point_to_a_CSV_file.save_data_point(
        ID=ID,
        Laserleistung=Laserleistung,
        Vorschubgeschwindigkeit=Vorschub,
        Fokusabstand=Fokusabstand,
        Düsenabstand=Düsenabstand,
        Düsenduchmesser=Düsendurchmesser,
        Gasdruck=Gasdruck,
        Schneidgasart=Schneidgasart,
        Schneidgasmischungsverhältnis=Scneidgasmischungsverhältnis,
        Material=Material,
        Materialstärke=Materialstärke,
        Abschnittbreite=Abschnittbreite,
        Schnittlänge=Schnittlänge,
        Abbildungsverhältnis=Abbildungsverhältnis,
        Laserwellenlänge=Laserewellenlänge,
        Faserdurchmesser=Faserdurchmesser,
        Schnitt_durch=schnitt_durch,
        Rampenart=Rampenart,
        Rampenstartwert=Rampenstartwert,
        Rampenendwert=Rampenendwert,
        Verstärkungsfaktor=Verstärkungsfaktor_LWM,
        RZ=RZ,
        Rm=RM,
        Ra=RA,
        Rq=Rq,
        Rp=Rp,
        Rv=Rv,
        Rsk=Rsk,
        Rku=Rku,
        Sm=Sm,
        Sk=Sk,
        Maximale_Barthöhe=max_y_range,
        Std_barthöhe=std_deviation,
        Tischposition_Nr=Tischposition,
        reward = reward,
        reward_func=reward_func,
        Modus=Modus,
        Bemerkung = Bemerkung

    )
    ID = int(ID) + 1
    print("Neue ID: ", ID)