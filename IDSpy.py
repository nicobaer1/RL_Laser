# Importieren der benötigten Module
from ids_peak import ids_peak
from ids_peak import ids_peak_ipl_extension
from ids_peak_ipl import ids_peak_ipl
from colorama import Fore, Style
import os
def capture_images_from_camera(id):


    # IDS-Bibliothek initialisieren
    ids_peak.Library.Initialize()

    # Device-Manager-Objekt erstellen
    device_manager = ids_peak.DeviceManager.Instance()

    try:
        # Device-Manager aktualisieren
        device_manager.Update()

        # Programm beenden, wenn kein Gerät gefunden wurde
        if device_manager.Devices().empty():
            print(f"{Fore.RED}Kein Gerät gefunden. Programm wird beendet{Style.RESET_ALL}.")
            return
        selected_device = 0
        device = device_manager.Devices()[selected_device].OpenDevice(ids_peak.DeviceAccessType_Control)

        sensor_name = device.ModelName()
        print(f"Der Sensor {Fore.BLUE}{sensor_name}{Style.RESET_ALL} wird verwendet.")

        # Basisordner für die Bildspeicherung
        base_folder = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_Bilder_IDS"




        image_index = id
        for i in range(10):
            exposure_time = 9500 + i * 3500  # Beispiel für eine lineare Steigerung der Belichtungszeit
            capture_image(device, base_folder, exposure_time, image_index)
            print("exposure_time",exposure_time)

        print(f"Bilder wurden in {os.path.join(base_folder, f'{Fore.BLUE}Bildreihe_{image_index}{Style.RESET_ALL}')} aufgenommen")
        print(f"Bilder wurden in {Fore.BLUE}Bildreihe_{image_index}{Style.RESET_ALL} aufgenommen")

    except Exception as e:
        print("Exception: " + str(e))

    finally:
        # IDS-Bibliothek schließen
        ids_peak.Library.Close()


def capture_image(device, folder_path, exposure_time, image_index):
    # Remote-Nodemap des Geräts abrufen
    nodemap_remote_device = device.RemoteDevice().NodeMaps()[0]

    # Kameraeinstellungen setzen
    nodemap_remote_device.FindNode("ExposureTime").SetValue(exposure_time)
    nodemap_remote_device.FindNode("AcquisitionMode").SetCurrentEntry("SingleFrame")

    # Bildaufnahme starten
    data_stream = device.DataStreams()[0].OpenDataStream()
    payload_size = nodemap_remote_device.FindNode("PayloadSize").Value()
    num_buffer = data_stream.NumBuffersAnnouncedMinRequired()

    for _ in range(num_buffer):
        buffer = data_stream.AllocAndAnnounceBuffer(payload_size)
        data_stream.QueueBuffer(buffer)

    data_stream.StartAcquisition()
    nodemap_remote_device.FindNode("AcquisitionStart").Execute()
    nodemap_remote_device.FindNode("AcquisitionStart").WaitUntilDone()

    try:
        # Aufgenommenes Bild verarbeiten und speichern
        result_buffer = data_stream.WaitForFinishedBuffer(5000)
        ipl_image = ids_peak_ipl_extension.BufferToImage(result_buffer)
        converted_ipl_image = ipl_image.ConvertTo(ids_peak_ipl.PixelFormatName_RGBa8)

        # Ordner für Bildreihe erstellen, falls nicht vorhanden
        image_folder = os.path.join(folder_path, f"Bildreihe_{image_index}")

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Dateipfad für das Bild erstellen
        filename = os.path.join(image_folder, f"Bild_{image_index}_exposure{exposure_time}.jpg")

        # Bild speichern
        ids_peak_ipl.ImageWriter.WriteAsJPG(filename, converted_ipl_image)

    except Exception as e:
        print(f"{Fore.RED}Fehler beim Empfangen oder Verarbeiten des Bildes:{Style.RESET_ALL}", e)
        return
    finally:
        data_stream.QueueBuffer(result_buffer)
