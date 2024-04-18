import os
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import plotly.graph_objs as go
import time
import matplotlib

def reward(id):

    file_folder = r'\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\07_Datenbank_Parameter_CutAIye\Datenbank_3D_Punktewolke_MicroEpsilon\3D_Daten_Umbenannt'
    file_name = str(id) + '.asc'
    file_path = os.path.join(file_folder, file_name)

    while True:
        if os.path.isfile(file_path ):
            print("Die Datei wurde im angegebenen Verzeichnis gefunden.")
            break  # Die Schleife verlassen, wenn die Datei gefunden wurde
        else:
            print("Die Datei fehlt im angegebenen Verzeichnis.")
            user_input = input("Wurde die Datei abgespeichert? (ja/nein): ").lower()
            if user_input == 'ja':
                continue  # Die Schleife erneut durchlaufen, um erneut nach der Datei zu suchen
            elif user_input == 'nein':
                print("Bitte speichern Sie die Datei ab und starten Sie das Programm erneut.")
                exit()  # Das Programm beenden, wenn der Benutzer angibt, dass die Datei nicht abgespeichert wurde
            else:
                print("Ungültige Eingabe. Bitte antworten Sie mit 'ja' oder 'nein'.")

    # Daten aus der ASCII-Datei lesen
    x, y, z = [], [], []
    with open(file_path, 'r') as file:
        for line in file:
            spalten = line.split()
            x_val = float(spalten[0])
            if -20 <= x_val <= 20:  # Filtern von x-Werten zwischen -30 und 30
                x.append(x_val)
                y.append(float(spalten[1]))
                z.append(float(spalten[2]))

    # Ersten und letzten Wert von x, y und z ausgeben
    #print("Erster Wert von x:", x[0])
    #print("Erster Wert von y:", y[0])
    #print("Erster Wert von z:", z[0])
    #print("Letzter Wert von x:", x[-1])
    #print("Letzter Wert von y:", y[-1])
    #print("Letzter Wert von z:", z[-1])

    # Konvertieren Sie die Listen in NumPy-Arrays für die Berechnungen
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    # Farbskala für die Z-Werte festlegen
    colors = z

    # Erstellen des 3D-Scatterplots mit Plotly
    fig = go.Figure()

    # Hinzufügen des Scatterplots mit Farbskala für Z-Werte und minimaler Punktegröße
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers',
                               marker=dict(size=1, color=colors, colorscale='Viridis'),  # Farbskala für die Marker
                               name='3D Scatterplot'))

    # Anpassen der Achsenbeschriftungen und des Titels
    fig.update_layout(scene=dict(xaxis_title='X-Achse',
                                 yaxis_title='Y-Achse',
                                 zaxis_title='Z-Achse',
                                 xaxis_range=[-50, 50],  # X-Achse: Werte zwischen -50 und +50
                                 yaxis_range=[50, -50],  # Y-Achse: Werte zwischen +50 und -50 (umgekehrte Reihenfolge)
                                 zaxis_range=[50, -50]  # Z-Achse: Werte zwischen +50 und -50 (umgekehrte Reihenfolge)
                                 ),
                      title='3D Scatterplot')

    # Anpassen der Farbskala
    fig.update_layout(coloraxis=dict(colorbar=dict(title='Z-Werte')))

    # Anzeigen des Plots
    #fig.show()

    # Initialisiere den Zähler
    anzahl_y_im_bereich = 0

    # Iteriere durch die y-Werte und zähle diejenigen, die im Bereich zwischen -6 und -30 liegen
    for y_wert in y:
        if -30 < y_wert < -6:
            anzahl_y_im_bereich += 1

    # Gib die Anzahl der y-Werte im Bereich zwischen -6 und -30 aus
    #print("Anzahl der y-Werte im Bereich zwischen -6 und -30:", anzahl_y_im_bereich)
    # Höhenwerte berechnen
    höhen = z - np.min(z)

    # Rauheitstiefe berechnen (RZ)
    RZ = np.max(höhen) - np.min(höhen)

    # Mittelwert der Rauheitshöhen (RM)
    RM = np.mean(höhen)

    # Arithmetisches Mittel der absoluten Höhenwerte (RA)
    RA = np.mean(np.abs(höhen))

    # Quadrierter Mittelwert (Rq)
    Rq = np.sqrt(np.mean(höhen ** 2))

    # Maximale Rauheit (Rp)
    Rp = np.max(höhen) - np.min(höhen)

    # Vertikaler Abstand (Rv)
    Rv = np.max(z) - np.min(z)

    # Schiefe (Rsk)
    Rsk = np.mean((höhen - np.mean(höhen)) ** 3) / (np.std(höhen) ** 3)

    # Kurtosis (Rku)
    Rku = np.mean((höhen - np.mean(höhen)) ** 4) / (np.std(höhen) ** 4)

    # Kubische Rauheit (Sm)
    Sm = np.mean(np.abs(höhen) ** 3) ** (1 / 3)

    # Kurtosis der Steigung (Sk)
    dx = np.gradient(x)
    dy = np.gradient(y)
    dz = np.gradient(z)
    Steigungen = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    Sk = np.mean((Steigungen - np.mean(Steigungen)) ** 4) / (np.std(Steigungen) ** 4)

    # Ausgabe der Ergebnisse
    #print("RZ (Rauheitstiefe):", RZ)
    #print("RM (Mittelwert der Rauheitshöhen):", RM)
    #print("RA (Arithmetisches Mittel der absoluten Höhenwerte):", RA)
    #print("Rq (Quadrierter Mittelwert):", Rq)
    #print("Rp (Maximale Rauheit):", Rp)
    #print("Rv (Vertikaler Abstand):", Rv)
    #print("Rsk (Schiefe):", Rsk)
    #print("Rku (Kurtosis):", Rku)
    #print("Sm (Kubische Rauheit):", Sm)
    #print("Sk (Kurtosis der Steigung):", Sk)

    """     :param Rq (Quadrierter Mittelwert): Rq ist die Quadratwurzel aus dem Mittelwert der quadrierten Höhenwerte. Es charakterisiert die mittlere quadratische Abweichung der Oberfläche und ist ein Maß für die mittlere Streuung der Höhenwerte.
            Rp (Maximale Rauheit): Rp ist der maximale Abstand zwischen dem höchsten und niedrigsten Punkt auf der Oberfläche. Es gibt die maximale Höhenabweichung an.
            Rv (Vertikaler Abstand zwischen den höchsten und niedrigsten Punkten): Rv ist der vertikale Abstand zwischen dem höchsten und niedrigsten Punkt auf der Oberfläche. Im Gegensatz zu Rp wird bei der Berechnung von Rv die Tiefenmittellinie der Oberfläche berücksichtigt.
            Rsk (Schiefe): Rsk misst die Asymmetrie der Höhenverteilung um den Mittelwert. Ein positives Rsk deutet auf eine langgestreckte, rechtssteile Verteilung hin, während ein negatives Rsk auf eine langgestreckte, linkssteile Verteilung hinweist.
            Rku (Kurtosis): Rku misst die Steilheit oder Flachheit der Höhenverteilung im Vergleich zu einer Normalverteilung. Ein hoher Rku-Wert deutet auf eine steile Verteilung mit vielen Ausreißern hin, während ein niedriger Rku-Wert auf eine flache Verteilung hinweist.
            Rz ISO (ISO-Raumtiefe): Rz ISO ist ähnlich wie RZ, aber es wird der Bereich zwischen zwei bestimmten Tiefen festgelegt, um die relevanten Rauheitsmerkmale besser zu erfassen.
            Sm (Kubische Rauheit): Sm charakterisiert die kubische Oberflächenrauheit und ist das kubische Mittel der absoluten Abweichungen zwischen den Höhenwerten und dem Mittelwert.
            Sk (Kurtosis der Steigung): Sk misst die Steilheit oder Flachheit der Steigungsverteilung. Es gibt an, ob die Steigungsverteilung eher flach oder spitz ist.
            Sp (Spektrenparameter): Sp bezieht sich auf verschiedene Parameter, die aus der Fourier-Analyse der Oberflächenrauheit gewonnen werden, wie beispielsweise die dominanten Wellenlängen und die Hauptwellenrichtungen."""
    # Eindeutige x-Werte finden und sortieren
    unique_x = np.unique(x)

    # Liste für die Abstände initialisieren
    y_ranges = []

    # Für jeden eindeutigen x-Wert den Abstand vom größten zum kleinsten y-Wert bestimmen
    for unique_x_val in unique_x:
        # Indizes für die aktuellen x-Werte erhalten
        indices = np.where(x == unique_x_val)[0]

        # y-Werte für die aktuellen x-Werte erhalten
        y_values = y[indices]

        # Abstand vom größten zum kleinsten y-Wert bestimmen
        y_range = np.max(y_values) - np.min(y_values)

        # Abstand zur Liste hinzufügen
        y_ranges.append(y_range)

    # Maximale Distanz ermitteln
    max_y_range = np.max(y_ranges)

    # Standardabweichung berechnen
    std_deviation = np.std(y_ranges)

    # Ausgabe des maximalen Abstands
    #print("Maximaler Abstand zwischen dem größten und dem kleinsten y-Wert für alle x-Werte:", max_y_range)
    #print("Standardabweichung der Abstände:", std_deviation)

    # Eindeutige x-Werte und zugehörige Abstände initialisieren
    unique_x_values = []
    y_ranges = []

    # Für jeden eindeutigen x-Wert den Abstand vom größten zum kleinsten y-Wert bestimmen
    for unique_x_val in unique_x:
        # Indizes für die aktuellen x-Werte erhalten
        indices = np.where(x == unique_x_val)[0]

        # y-Werte für die aktuellen x-Werte erhalten
        y_values = y[indices]

        # Abstand vom größten zum kleinsten y-Wert bestimmen
        y_range = np.max(y_values) - np.min(y_values)

        # Eindeutigen x-Wert und zugehörigen Abstand speichern
        unique_x_values.append(unique_x_val)
        y_ranges.append(y_range)

    # Plot erstellen
    plt.figure(figsize=(10, 6))
    plt.plot(unique_x_values, y_ranges, marker='o',markersize=4, linestyle='-')
    plt.xlabel('x-Werte')
    plt.ylabel('Abstand zwischen größtem und kleinstem y-Wert')
    plt.title('Abstand zwischen größtem und kleinstem y-Wert für jede x-Wert')

    # Maximalen Wert markieren
    max_index = np.argmax(y_ranges)
    max_x_val = unique_x_values[max_index]
    max_y_val = y_ranges[max_index]
    #plt.plot(max_x_val, max_y_val, marker='o', markersize=2, color='red')
    #plt.text(max_x_val, max_y_val, f'   Max: ({max_x_val}, {max_y_val})', fontsize=12, color='red')

    # Durchschnitt anzeigen
    average_y_range = np.mean(y_ranges)
    #plt.axhline(y=average_y_range, color='r', linestyle='--', label='Durchschnitt: {:.2f}'.format(average_y_range))
    #plt.legend()
    #matplotlib.pyplot.close()
    #print("Summe y-Werte:", sum(y_ranges)/len(y_ranges))
    #plt.grid(True)
    plt.show()
    print("Plot")

    reward=-(sum(y_ranges)/len(y_ranges))+10
    #print("Reward",reward)
    #reward = -(RZ+RM+Rp+(10*(max_y_range+std_deviation+average_y_range)))
    #reward = -(anzahl_y_im_bereich)
    #print("Reward",reward)
    #reward_func = "-(RZ + RM + Rp + (10 * (max_y_range + std_deviation + average_y_range)))"
    reward_func = "-(sum(y_ranges)/len(y_ranges))+10"
    #reward_func = "-Anzahl der y-Werte im Bereich zwischen -6 und -30:"
    #print("Reward:",reward)

    return reward, RZ, RM, RA, Rq,Rp, Rv,Rsk, Rku,Sm, Sk , max_y_range,std_deviation, reward_func

def messung_durchgefuehrt():
    # Hier würde die tatsächliche Überprüfung stattfinden, ob die Messung durchgeführt wurde
    # Diese Funktion sollte entsprechend deiner tatsächlichen Logik implementiert werden
    return input("Ist die Messung durchgeführt worden? (ja/nein): ").lower().strip() == "ja"
