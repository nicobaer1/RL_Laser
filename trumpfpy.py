def TLC_start_cutting():

    mpf_content_warten = '''

            G04 F1
            R100 = 0        
            G04 F1

            RESET_EXT_ANST
            M17
            '''

    # Pfad zur .mpf-Datei
    file_path_WARTEN = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Aufträge\Schneidaufträge\Neu\Baer\AA\G_Code_RL\WARTEN_RL.mpf"

    # Datei erstellen und Inhalt speichern
    with open(file_path_WARTEN, "w") as f:
        f.write(mpf_content_warten)

        print("start_cutting")


def TLC_end_cutting():
    mpf_content_warten = '''

            G04 F1
            R100 = 1     
            G04 F1

            RESET_EXT_ANST

            M17


            '''

    # Pfad zur .mpf-Datei
    file_path_WARTEN = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Aufträge\Schneidaufträge\Neu\Baer\AA\G_Code_RL\WARTEN_RL.mpf"


    # Datei erstellen und Inhalt speichern
    with open(file_path_WARTEN, "w") as f:
        f.write(mpf_content_warten)

        print("TLC_end_cutting")

def G_Code_parameterübergabe (Laserleistung:float,Gasdruck:float,Vorschub:float,x_start:float,y_start:float,z_start:float,x_end:float, y_end:float, z_end:float,Schneidgasart:str):
    Schneidgasart = Schneidgasart
    while True:
        if Schneidgasart.lower() == "stickstoff":
            parameter_schneidgasart = 2
            break
        elif Schneidgasart.lower() == "sauerstoff":
            parameter_schneidgasart = 1
            break
        else:
            print("Ungültige Eingabe für Schneidgasart. Bitte geben Sie entweder 'Stickstoff' oder 'Sauerstoff' ein.")
            Schneidgasart = input("Bitte geben Sie die Schneidgasart ein (Stickstoff oder Sauerstoff): ")

    x_start,y_start,z_start = check_axis_params_start(x_start=x_start, y_start=y_start, z_start=z_start)
    #print("Startwerte: x_start:", x_start, " y_start:", y_start, " z_start:", z_start)
    x_end, y_end,z_end= check_axis_params_end(x_end=x_end, y_end=y_end, z_end=z_end)
    #print("Endwerte: x_end:", x_end, " y_end: ", y_end, " z_end:", z_end)

    """# Hier können Sie die Parameter verwenden oder zurückgeben
    print("Der Parameter für die Schneidgasart lautet:", parameter_schneidgasart)
    print("Laserleistung:", Laserleistung)
    print("Gasdruck:", Gasdruck)
    print("Vorschub:", Vorschub)"""
    print("Startposition x:", x_start," y:", y_start,"z:",z_start)

    # Hier können Sie den Rest Ihres Codes einfügen oder die Parameter zurückgeben

    def funktion_mit_parameter_Gasdruck(parameter):
        #print("Übergebener Gasdruck",parameter)
        if parameter < 3000:
            print("Der Parameter Gasdruck darf nicht kleiner als 3000 sein. Der Wert wird auf 3000 gesetzt.")
            parameter = 3000
        # Führen Sie hier den restlichen Code Ihrer Funktion aus
        #print("Der aktueller Gasdruck:", parameter)

    funktion_mit_parameter_Gasdruck(Gasdruck)
    #print("Check_gasdruck")
    print("Laserleistung",Laserleistung)
    Laserleistung_in_Volt = Laserleistung * 1.25
    #print("Laserleistung_Volt",Laserleistung_in_Volt)

    'Schreiben des G-Codes und Abspeichern als mpf'
    mpf_content = '''
                ;Laserleistung
                DEF REAL x_start, y_start, z_start, Laserleistung, Gasdruck, Vorschub
                EXTERN GLB_LASEREIN(INT,INT,INT,INT,INT,INT,INT)
                EXTERN GLB_LASEREIN2(INT, INT, INT, INT)
                EXTERN YAG_PRECITEC_CUT_POLY2(INT,REAL,INT,REAL,REAL)
                EXTERN GLB_TEXT_WELD_YAG(STRING[80],STRING[24],REAL)
                N20 DEF INT TRUMPFPRG_EINSTECHEN
                N25 DEF INT TRUMPFPRG_SCHNEIDEN
                N30 DEF INT SCHNEIDGESCHWINDIGKEIT

                N35 DEF INT SCHNEIDGASART ;  1: O2, 2: N2
                SCHNEIDGASART =''' + str(parameter_schneidgasart) + '''         

                ;     Punkt  Kanal   Spannung(mV 10V=100%)     Zeit         Sollwert
                G820 S0=1   S1=1    H10=10                                 H40=FIX
                G820 S0=2   S1=1    H10=1600                               H40=FIX
                G820 S0=3   S1=1    H10=10                                 H40=FIX

                N55 R01=''' + str(Laserleistung_in_Volt) + '''; LEISTUNGSVORGABE IN W TRUDISK8001 SCHNEIDEN
                N60 R02=''' + str(Gasdruck) + '''; DRUCK SCHNEIDEN IN MBAR
                N65 SCHNEIDGESCHWINDIGKEIT = ''' + str(Vorschub) + ''' ;1500; MM/MIN VORSCHUB SCHNEIDEN                
                N90 TRUMPFPRG_EINSTECHEN = 67 ; VORSICHT !
                N95 TRUMPFPRG_SCHNEIDEN = 5 ; VORSICHT ! 
                N105 F5000
                TC_ELEMENT_STATE_1(1,0); Crossjet ein
                N120 TC_OVL(8) ; IRGENDWAS MIT BESCHLEUNIGUNG
                N135 SET_G54(''' + str(x_start) + ''',''' + str(y_start) + ''',''' + str(z_start) + ''',0,-90,0); ALTERNATIV ZU SET_POS(0,0,0) FüR ABSOLUTKOORDINATEN

                N150 GLB_LASERANF; LASERANFORDERUNG
                N155 TC_ELEMENT_STATE_1(2,0); KENNLINIE 1 AUF 1
                N275 TC_ELEMENT_STATE_1(8,0); WECHESEL AUF KENNLINIE 2 
                 
                TC_ELEMENT_STATE_2(1,0); Crossjet aus   

                N230 CONT1: MSG("CONT1")
                N235 G1 X0 Y0
                N240 G01 Z0        
                N270 ; SCHNEIDEN        
                N280 TC_IFSW_GAS_2(SCHNEIDGASART,R02)  ; 1: O2, 2: N2
                N285 F = SCHNEIDGESCHWINDIGKEIT
                TC_ELEMENT_STATE_1(1,0); Crossjet ein
                N290 GLB_LASEREIN2(R01,TRUMPFPRG_SCHNEIDEN,1,1); LEISTUNG, LASERPROG, W1H, ACL           
                N300 G1 X''' + str(x_end) + ''' Y''' + str(y_end) + ''' Z''' + str(z_end) + ''' 
                N305 GLB_LASERAUS 
                TC_ELEMENT_STATE_2(1,0); Crossjet aus
                N310 F10000 ; VERFAHRGESCHWINDIGKEIT
                N315 G01 Z40
                N320 TC_ELEMENT_STATE_2(8,0); WECHSEL AUF KENNLINIE 1
                ;ENTRY_LASER:
                N325 CONT2: MSG("CONT2")           
                N330 G1 X0 Y0 
                N335 TC_LASER_OFF(2) ;LASER AUS STRAHLFALLE ZU UND GAS AUS
                N360 TC_IFSW_LASERANFORDERUNG(0); LASERABGEBEN (0) LASER 1-7   
                RESET_EXT_ANST
                M17        
                '''

    # Pfad zur .mpf-Datei
    file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Aufträge\Schneidaufträge\Neu\Baer\AA\G_Code_RL\Parameter_RL.mpf"

    'Abfrage ob TLC 7040 den Versuch durchgeführt hat'
    # Datei erstellen und Inhalt speichern
    with open(file_path, "w") as f:
        f.write(mpf_content)
    print("G-Code erstellt")







def check_axis_params_start(x_start=None, y_start=None, z_start=None):
    min_value_x_start = 2324
    max_value_x_start = 2465
    min_value_y_start = 1080
    max_value_y_start = 1230
    min_value_z_start = 252
    max_value_z_start = 300

    while True:
        if (x_start is None or min_value_x_start <= x_start <= max_value_x_start) \
                and (y_start is None or min_value_y_start <= y_start <= max_value_y_start) \
                and (z_start is None or min_value_z_start <= z_start <= max_value_z_start):
            #print("Alle Parameter sind im Bereich.")
            return x_start, y_start, z_start  # Rückgabe der Parameter, auch wenn sie nicht aktualisiert wurden
        else:
            print("Mindestens ein Parameter liegt außerhalb des Bereichs.")
            print("Bitte aktualisiere die Parameter.")
            x_start = input_with_range_check("x_start", min_value_x_start, max_value_x_start)
            y_start = input_with_range_check("y_start", min_value_y_start, max_value_y_start)
            z_start = input_with_range_check("z_start", min_value_z_start, max_value_z_start)



def check_axis_params_end(x_end=None, y_end=None, z_end=None):
    min_value_x_end = 0
    max_value_x_end = 140
    min_value_y_end = 0
    max_value_y_end = 0
    min_value_z_end = 0
    max_value_z_end = 5

    while True:
        if (x_end is None or min_value_x_end <= x_end <= max_value_x_end) \
                and (y_end is None or min_value_y_end <= y_end <= max_value_y_end) \
                and (z_end is None or min_value_z_end <= z_end <= max_value_z_end):
            #print("Alle Parameter sind im Bereich.")
            return x_end, y_end, z_end
        else:
            print("Mindestens ein Parameter liegt außerhalb des Bereichs.")
            print("Bitte aktualisiere die Parameter.")
            x_end = input_with_range_check("x_end", min_value_x_end, max_value_x_end)
            y_end = input_with_range_check("y_end", min_value_y_end, max_value_y_end)
            z_end = input_with_range_check("z_end", min_value_z_end, max_value_z_end)
    return x_end, y_end, z_end

def input_with_range_check(param_name, min_value, max_value):
    while True:
        try:
            value = int(input(f"Geben Sie einen neuen Wert für {param_name} ({min_value}-{max_value}): "))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Der eingegebene Wert für {param_name} liegt außerhalb des Bereichs.")
        except ValueError:
            print("Bitte geben Sie eine ganze Zahl ein.")






