import os
import shutil

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

# Beispielaufruf
rename_and_move_file("3119")  # ID als String übergeben
