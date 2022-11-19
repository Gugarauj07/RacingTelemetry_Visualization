from threading import Event, Thread
import serial
import serial.tools.list_ports
from time import strftime
from pathlib import Path
import csv
import pandas as pd
import gc
from random import randrange

serialPort = serial.Serial()
serialPort.timeout = 0.5

arquivo = strftime("%d.%m.%Y_%Hh%M")
path = Path("Arquivos_CSV")
path.mkdir(parents=True, exist_ok=True)
with open(f"Arquivos_CSV/{arquivo}.csv", 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(
        ['tempo', 'temp_obj', 'temp_amb', 'RPM_motor', 'RPM_roda', 'capacitivo', 'VEL_D', 'VEL_E', 'ACC', 'Distancia',
         'button_lap'])
portList = [port.device for port in serial.tools.list_ports.comports()]

# TESTING
N = 100
sensors = {
    'tempo': [],
    'temp_obj': [],
    'temp_amb': [],
    'RPM_motor': [],
    'VEL_E': [],
    'capacitivo': [],
    'button_lap': [],
    'ACC': [],
    'RPM_roda': [],
    'Distancia': [],
    'VEL_D': [],
}
df = pd.DataFrame(sensors)


# ======================================
def read_serial(n):
    VEL, counter_laps, tempo_inicio = 0, 0, 0

    tempo = n
    temp_obj = randrange(40, 60)
    temp_amb = randrange(50, 60)
    RPM = randrange(600, 800)
    VEL = randrange(20, 30)
    capacitivo = randrange(0, 3)
    button = randrange(0, 3)

    VEL_anterior = VEL
    # tempo, temp_obj, temp_amb, RPM, VEL, capacitivo, button = serialPort.readline().decode("utf-8").split(',')
    Distancia = VEL / 3.6  # Metros
    ACC = VEL - VEL_anterior
    RPMroda = VEL / ((18 / 60) * 0.04625 * 1.72161199 * 3.6)
    line = [tempo, temp_obj, temp_amb, RPM, VEL, capacitivo, button, ACC, RPMroda, Distancia, 0]
    df.loc[len(df)] = line
    # df["tempo"] = tempo
    # df["temp_obj"] = temp_obj
    # df["temp_amb"] = temp_amb
    # df["RPM"] = RPM
    # df["VEL"] = VEL
    # df["capacitivo"] = capacitivo
    # df["button"] = button
    # df["ACC"] = ACC
    # df["RPMroda"] = RPMroda
    # df["Distancia"] = Distancia

    # df_tempo = df.loc[df["tempo"] == tempo_inicio:df["tempo"] == tempo]
    # acc_avg = df_tempo["ACC"].mean()
    # vel_avg = df_tempo["VEL"].mean()
    # distancia_lap = df_tempo["Distancia"].head(1) - df_tempo["Distancia"].tail(1)
    # tempo_percorrido = df_tempo["tempo"].head(1) - df_tempo["tempo"].tail(1)
    #
    # if button != counter_laps:
    #     tempo_inicio = tempo
    #     counter_laps = button

    with open(f"Arquivos_CSV/{arquivo}.csv", 'a+', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(line)

    gc.collect()


def connect_serial(self):
    serialPort.port = portList[0]
    serialPort.baudrate = 9600

    try:
        serialPort.open()  # Tenta abrir a porta serial
    except:
        print("ERROR SERIAL")