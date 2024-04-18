import pyads
import time
import IDSpy
import os
import shutil
from colorama import Fore, Style


plc = pyads.Connection('127.0.0.1.1.1', pyads.PORT_TC3PLC1)
plc.open()
def GVL_Achse (axis_number,new_value_axis):
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    variable_name_alarm = "GVL_Achse_0" + str(axis_number) + ".E_Alarm"
    read_variable_name_alarm = plc.read_by_name(variable_name_alarm)

    variable_achse_ist_bereit= "GVL_Achse_0" + str(axis_number) + ".E_ist_Bereit"
    read_variable_achse_ist_bereit= plc.read_by_name(variable_achse_ist_bereit)
    if read_variable_achse_ist_bereit ==False:
        print("Achse "+str(axis_number)+" ist nicht Bereit")
    else:
        print("Achse " + str(axis_number) + " ist Bereit")


    if read_variable_name_alarm==True:
        variable_name_alarm_code = "GVL_Achse_0" + str(axis_number) + ".EW_Alarm_Code"
        read_variable_name_alarm_code = plc.read_by_name(variable_name_alarm_code)
        print("Alarmcode",str(read_variable_name_alarm_code))
    else:



        """Diese Funktion übergibt der Achse die neue Postition"""
        #Achse freigeben
        variable_name = "GVL_Achse_0" + str(axis_number) + ".A_Freigabe"  # Geben Sie den vollständigen Pfad zur Variable an
        new_value = True  # Der Wert, den Sie schreiben möchten
        plc.write_by_name(variable_name, new_value)
        #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

        #Achse Position vorgeben
        variable_name = "GVL_Achse_0"+str(axis_number)+".ADW_Soll_pos"  # Geben Sie den vollständigen Pfad zur Variable an
        # Der Wert, den Sie schreiben möchten
        new_value=new_value_axis
        plc.write_by_name(variable_name, new_value)
        #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")


        variable_name = "GVL_Achse_0"+str(axis_number)+".A_Move"  # Geben Sie den vollständigen Pfad zur Variable an
        new_value = True  # Der Wert, den Sie schreiben möchten
        plc.write_by_name(variable_name, new_value)
        #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

        while True:
            # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
            variable_name_read = "GVL_Achse_0" + str(axis_number) + ".EDW_Ist_pos"
            value_read = plc.read_by_name(variable_name_read)
            if new_value_axis == value_read:
                variable_name = "GVL_Achse_0" + str(axis_number) + ".A_Move"  # Geben Sie den vollständigen Pfad zur Variable an
                new_value = False  # Der Wert, den Sie schreiben möchten
                plc.write_by_name(variable_name, new_value)
                # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
                # Achse freigeben beenden
                variable_name = "GVL_Achse_0" + str(axis_number) + ".A_Freigabe"  # Geben Sie den vollständigen Pfad zur Variable an
                new_value = False  # Der Wert, den Sie schreiben möchten
                plc.write_by_name(variable_name, new_value)
                break  # Schleife beenden, wenn die Bedingung erfüllt ist
            else:
                """"print(f"Gelesener Wert: {value_read}. Warte auf den Zielwert: {new_value_axis}")"""


    #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    variable_name = "GVL_Achse_0" + str(axis_number) + ".EDW_Ist_pos"
    value_read = plc.read_by_name(variable_name)
    print(str(variable_name) + ":", value_read)

def MAIN_Positionswechsel_Tisch(repettitions):
    # Zeit vor dem Stoppen
    start_time = time.time()

    for _ in range(repettitions):
        variable_name = "MAIN.Positionswechsel_Tisch"  # Geben Sie den vollständigen Pfad zur Variable an
        new_value = True  # Der Wert, den Sie schreiben möchten
        plc.write_by_name(variable_name, new_value)
        #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

        time.sleep(1)
        new_value = False  # Der Wert, den Sie schreiben möchten
        plc.write_by_name(variable_name, new_value)
        time.sleep(2)
        #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    new_value = False  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    #print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    # Zeit nach dem Stoppen
    end_time = time.time()
    # Berechnung der verstrichenen Zeit
    elapsed_time = end_time - start_time

    # Ausgabe der verstrichenen Zeit
    print(f"Die verstrichene Zeit beträgt: {elapsed_time} Sekunden.")


def read_variable (variable_name: str):

    # Variable lesen
    value_read= plc.read_by_name(variable_name)
    print(str(variable_name)+":",value_read)

def achse_referenzfahrt (axis_number:int):
    """Diese Funktion führt eine Referenzfahrt durch"""
    # Achse freigeben
    variable_name = "GVL_Achse_0" + str(axis_number) + ".A_Referenzfahrt"
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    time.sleep(1)
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    # Variable lesen
    variable_name = "GVL_Achse_0" + str(axis_number) + ".EDW_Ist_pos"
    value_read = plc.read_by_name(variable_name)
    print(str(variable_name) + ":", value_read)




def düsenabstand (düsenabstand):
    variable_name = "MAIN.Duesenabstand_soll_mm"
    new_value = düsenabstand  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)


def fokusabstand (fokusabstand):
    variable_name = "MAIN.Fokuslage_soll_mm"
    new_value = fokusabstand  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)

def ventilator():
    variable_name = "MAIN.Ventilator"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)


def Sensor3D_automatisch(y_start,ID):

    variable_name = "MAIN.Trigger_IDS_Kamera_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = False  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    wert= 1232
    position = int((wert-y_start)*100)
    print("Position",position)
    GVL_Achse(4, position)
    print(Fore.BLUE + "3D Sensor Ordner leeren" + Style.RESET_ALL)
    delete_folder_contents()
    time.sleep(3)

    print(Fore.BLUE + "3D Sensor macht aufnahme" + Style.RESET_ALL)
    variable_name = "MAIN.Trigger_3D_Sensor"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    time.sleep(1)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    variable_name = "MAIN.Trigger_3D_Sensor"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = False # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    time.sleep(7)
    GVL_Achse(4, 0)
    time.sleep(2)
    rename_and_move_file(ID)
def Trigger_IDS_Kamera_Beleuchtung_EIN():
    variable_name = "MAIN.Trigger_IDS_Kamera_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

def Trigger_IDS_Kamera_Beleuchtung_AUS():
    variable_name = "MAIN.Trigger_IDS_Kamera_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = False  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

def Trigger_TLC_Beleuchtung_EIN():
    variable_name = "MAIN.Trigger_TLC_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")

def Trigger_TLC_Beleuchtung_AUS():
    variable_name = "MAIN.Trigger_TLC_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = False  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")


def IDS_Kamera_automatisch(y_start,ID):
    variable_name = "MAIN.Trigger_IDS_Kamera_Beleuchtung"  # Geben Sie den vollständigen Pfad zur Variable an
    new_value = True  # Der Wert, den Sie schreiben möchten
    plc.write_by_name(variable_name, new_value)
    # print(f"Variable '{variable_name}' erfolgreich auf {new_value} gesetzt.")
    wert= 1232

    position = int((wert-y_start)*100)
    print("Position",position)
    GVL_Achse(3, position)
    time.sleep(3)
    IDSpy.capture_images_from_camera(ID)
    time.sleep(1)
    GVL_Achse(3, 0)
    

'''
def rename_and_move_file(ID):
    source_directory = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Sensor"
    destination_directory = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Umbenannt"

    # Konstruiere den vollen Pfad für die einzige .asc-Datei im Quellverzeichnis
    source_file_path = os.path.join(source_directory, os.listdir(source_directory)[0])

    # Konvertiere die ID in einen String und konstruiere den vollen Pfad für die Zieldatei
    ID_str = str(ID)
    destination_file_path = os.path.join(destination_directory, ID_str + ".asc")

    # Umbenennen und Verschieben der Datei
    shutil.move(source_file_path, destination_file_path)

    print(f"Datei umbenannt und verschoben: {source_file_path} -> {destination_file_path}")
'''

def rename_and_move_file(ID):
    source_directory = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Sensor"
    destination_directory = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Umbenannt"

    files = os.listdir(source_directory)

    if not files:
        print("Keine Dateien im Verzeichnis gefunden.")
        retry = input("Möchten Sie es erneut versuchen? (ja/nein): ")
        if retry.lower() == "ja":
            rename_and_move_file(ID)
        else:
            print("Operation abgebrochen.")
            return

    # Konstruiere den vollen Pfad für die einzige .asc-Datei im Quellverzeichnis
    source_file_path = os.path.join(source_directory, files[0])

    # Konvertiere die ID in einen String und konstruiere den vollen Pfad für die Zieldatei
    ID_str = str(ID)
    destination_file_path = os.path.join(destination_directory, ID_str + ".asc")

    # Umbenennen und Verschieben der Datei
    shutil.move(source_file_path, destination_file_path)

    print(f"Datei umbenannt und verschoben: {source_file_path} -> {destination_file_path}")


def delete_folder_contents():
    folder_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Sensor"

    try:
        # Überprüfen, ob der Ordner existiert
        if os.path.exists(folder_path):
            # Alle Dateien und Unterverzeichnisse im Ordner löschen
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # Wenn es sich um einen Ordner handelt, rekursiv löschen
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                # Wenn es sich um eine Datei handelt, löschen
                else:
                    os.remove(file_path)
            print(f"Inhalt des Ordners {folder_path} erfolgreich gelöscht.")
        else:
            print(f"Der Ordner {folder_path} existiert nicht.")
    except Exception as e:
        print(f"Fehler beim Löschen des Ordners: {e}")


MAIN_Positionswechsel_Tisch(6)
#Trigger_IDS_Kamera_Beleuchtung_AUS()
#Trigger_TLC_Beleuchtung_AUS()
#MAIN_Positionswechsel_Tisch(3)

#Sensor3D_automatisch(1225,0)